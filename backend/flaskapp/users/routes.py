import jwt
import datetime
from flaskapp.db_models import User
from flaskapp.users.messages import send_otp
from flaskapp import redis_client, bcrypt, db
from flaskapp.users.utils import generate_otp
from flaskapp.utils import login_required, logout_required
from flask import Blueprint, jsonify, request, current_app

users_bp = Blueprint("users", __name__)

@users_bp.route("/sign-up/", methods=["POST"])
@logout_required
def sign_up():
	response = request.get_json()
	name = response.get('name')
	email = response.get('email')

	# handle empty payload
	if not name or not email:
		return jsonify({'error': 'Name and email are required.'}), 400

	# Check if username and email already exist
	errors = {}
	if User.check_name(name):
		errors['nameStatus'] = 'Username already taken.'

	if User.check_email(email):
		errors['emailStatus'] = 'Email already taken.'

	# 409 Conflict for duplicate entries
	if errors:
		return jsonify(errors), 409

	# Generate OTP and send it
	otp = generate_otp()
	is_sent = send_otp(otp, email)

	if not is_sent:
		return jsonify({"error": "Failed to send OTP."}), 500
	
	# if email sent than store the otp with email for 2 minutes
	redis_client.setex(email, 120, otp)

	return jsonify({"message": "OTP sent to email."}), 200


# verify signup otp and store the user in the database
@users_bp.route('/verify/', methods=['POST'])
@logout_required
def verify():
	response = request.get_json()
	otp = response.get('otp')
	name = response.get('name')
	email = response.get('email')
	password = response.get('password')

	# handle empty payload
	if not name or not email or not otp or not password:
		return jsonify({'error': 'Invalid credentials!'}), 400

	# check stored otp for given email in redis cache
	stored_otp = redis_client.get(email)
	if not stored_otp:
		return jsonify({"error": "Timeout or invalid OTP."}), 400

	if stored_otp == otp:
		# in verification process if other user take the username
		if not (User.check_name(name) and User.check_email(email)):
			hashed_pass = bcrypt.generate_password_hash(password, rounds=13).decode('utf-8')
			name = name.strip().replace(' ', '-').lower()
			user = User(username=name, email=email, password=hashed_pass)
			db.session.add(user)
			db.session.commit()
			redis_client.delete(email)
			return jsonify({"message": "Signup successful."}), 200

		# username email taken while sign up
		return jsonify({"error": "Please check username and email again."}), 400

	return jsonify({"error": "Timeout or invalid OTP."}), 400

# login
@users_bp.route('/log-in/', methods=['POST'])
@logout_required
def log_in():
	response = request.get_json()
	email = response.get('email')
	password = response.get('password')

	# handle empty payload
	if not email or not password:
		return jsonify({"error": "Invalid credentials!"}), 401

	user = User.query.filter_by(email=email).first()
	if user and bcrypt.check_password_hash(user.password, password):
		token = jwt.encode(
			{'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['JWT_TIMEOUT'])},
			current_app.config['SECRET_KEY'], algorithm="HS256")
		return jsonify({"token": token}), 200
	
	return jsonify({"error": "Invalid credentials!"}), 401


# reset password
@users_bp.route("/reset-password/", methods=["POST"])
@logout_required
def reset_password():
	response = request.get_json()
	email = response.get("email")

	# handle empty payload
	if not email:
		return jsonify({"error": "Invalid credentials!"}), 400

	user = User.query.filter_by(email=email).first()
	if user:
		# Generate OTP and send it
		otp = generate_otp()
		is_sent = send_otp(otp, email)
		if not is_sent:
			return jsonify({"error": "Failed to send OTP."}), 500
		
		# if email sent than store the otp with email for 2 minutes
		redis_client.setex(email, 120, otp)
		return jsonify({"message": "OTP sent to email."}), 200
	
	return jsonify({"error": "Please check your email address."}), 400


# verify reset otp
@users_bp.route("/verify-reset-otp/", methods=["POST"])
@logout_required
def verify_reset_otp():
	response = request.get_json()
	email = response.get("email")
	otp = response.get("otp")

	# empty payload
	if not email or not otp:
		return jsonify({"error": "Invalid credentials!"}), 400

	# check stored otp for given email in redis cache
	stored_otp = redis_client.get(email)
	if stored_otp and stored_otp == otp:
		return jsonify({"message": "Otp matched."}), 200

	return jsonify({"error": "Timeout or invalid OTP."}), 400

# set new password
@users_bp.route("/new-password/", methods=["POST"])
@logout_required
def new_pass():
	response = request.get_json()
	email = response.get("email")
	otp = response.get("otp")
	password = response.get("pass")

	# handle empty payload
	if not email or not otp or not password:
		return jsonify({"error": "Invalid credentials!"}), 400

	# set new password
	# check stored otp for given email in redis cache
	stored_otp = redis_client.get(email)
	if stored_otp and stored_otp == otp:	
		user = User.query.filter_by(email=email).first()
		hashed_pass = bcrypt.generate_password_hash(password, rounds=13).decode('utf-8')
		user.password = hashed_pass
		db.session.commit()
		redis_client.delete(email)
		return jsonify({"message": "Password changed."}), 200

	return jsonify({"error": "Something went wrong!"}), 400

# account endpoint
@users_bp.route('/account/')
@login_required
def account(current_user):
	data = {
		"name": current_user.username,
		"email": current_user.email
	}

	return jsonify(data), 200