from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Profile
from . import db



auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods = ['POST'])
def login_post():
	# get info from form
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False
	# check for email
	user = User.query.filter_by(email=email).first()
	# check if password is correct
	if not user or not check_password_hash(user.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login'))
	
	login_user(user, remember=remember)
	return redirect(url_for('main.profile', identifier = current_user.id))



@auth.route('/signup')
def signup():
    return render_template('signup.html')



@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
	# get values filled in form
	email = request.form.get('email')
	name = request.form.get('name')
	password = request.form.get('password')
	gender = request.form.get('gender')
	# check if email exist
	user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
	if user: #if already one is there redirect to signup page
		flash('Email address already exists')
		return redirect(url_for('auth.signup'))
	# if new user adding the new user to database after hashing the passwords
	new_user = User(email=email, name=name, password = generate_password_hash(password, method='sha256'), gender=gender)
	db.session.add(new_user)
	db.session.commit()
	name_default_profile_pic = "img/default_{}.png".format(gender)
	# add id to profile table
	new_profile = Profile(user_id = new_user.id, name=new_user.name ,profile_pic_name = name_default_profile_pic, bio = "Pls write your Bio")
	db.session.add(new_profile)
	db.session.commit()

	return redirect(url_for('auth.login'))



@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))