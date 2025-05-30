import jwt
from functools import wraps
from flaskapp.db_models import User
from flask import request, current_app, jsonify

# protected route
def login_required(f):
	@wraps(f)
	def inner(*args, **kwargs):
		token = None
		auth_header = request.headers.get("Authorization")
		if not auth_header:
			return jsonify({"error": "Token is missing!"}), 401

		# check the secret to ensure only the request is coming only from our frontend 
		if auth_header.startswith(f'{current_app.config["AUTH_PREFIX"]}'):
			token = auth_header.split(" ")[1]

		# if no token found
		if not token:
			return jsonify({"error": "Token is missing!"}), 401

		# loading data from jwt can throw exceptions
		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
			current_user = User.query.filter_by(id=data.get('id')).first()
		except jwt.ExpiredSignatureError:
			return jsonify({"error": "Token has expired!"}), 401
		except jwt.InvalidTokenError:
			return jsonify({"error": "Invalid token!"}), 401

		# return user with args and kwargs to access in route
		return f(current_user, *args, **kwargs)
	return inner

# forbidden route for already authenticated user
def logout_required(f):
	@wraps(f)
	def inner(*args, **kwargs):
		if 'Authorization' in request.headers:
			return jsonify({"error": "Forbidden response!"}), 403
		return f(*args, **kwargs)
	return inner