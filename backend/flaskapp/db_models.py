from flaskapp import db
from datetime import datetime

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	# username check while creating account
	@staticmethod
	def check_name(name):
		name = name.strip().replace(' ', '-').lower()
		user = User.query.filter_by(username=name).first()
		return True if user else False

	# email check while creating account
	@staticmethod
	def check_email(email):
		user = User.query.filter_by(email=email).first()
		return True if user else False

	def __repr__(self):
		return f'username: {self.username} | email: {self.email}'