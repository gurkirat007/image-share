from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
	__tablename__="user"
	id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))
	gender = db.Column(db.String)

class Profile(db.Model):
	__tablename__="profile"
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
	profile_pic_name = db.Column(db.String)
	bio = db.Column(db.String)