# add follower following fuction
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import db
from .models import User, Profile, Followers, Posts

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}





def check_follow(profile_id):
	follower_data = Followers.query.filter(Followers.follower == current_user.id, Followers.following == profile_id).all()
	if follower_data:
		return True
	else:
		return False





def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
	people_follow_you_data = []
	people_you_follow_data = []
	if current_user.is_authenticated:
		people_you_follow = Followers.query.filter(Followers.follower == current_user.id).all()
		
		for people in people_you_follow:
			people_data = Profile.query.get(people.following)
			people_you_follow_data.append(people_data)


		people_follow_you= Followers.query.filter(Followers.following == current_user.id).all()
		
		for people in people_follow_you:
			people_data = Profile.query.get(people.follower)
			people_follow_you_data.append(people_data)

	return render_template('index.html', followings=people_you_follow_data, followers=people_follow_you_data)

# login required
@main.route('/profile/<identifier>')
@login_required
def profile(identifier):
	profile_page_data = Profile.query.get(identifier)

	return render_template('profile.html', profile_page_data = profile_page_data, status_following = check_follow(identifier))


@main.route('/editprofile')
@login_required
def editprofile():
	return render_template('edit_profile.html')



@main.route('/editprofile', methods = ['POST'])
@login_required
def edit_profile():
	# check if the post request has the file part
	if 'file' not in request.files:
		return redirect(url_for('main.profile', identifier = current_user.id))
	file = request.files['file']
	new_bio = request.form.get('bio')
	if file.filename == '':
		return redirect(url_for('main.profile', identifier = current_user.id))
	if file and allowed_file(file.filename):
		file_name = "pp_{}.{}".format(current_user.id, file.filename.rsplit('.', 1)[1].lower())
		filename = secure_filename(file_name)
		file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
	profile_data = Profile.query.get(current_user.id)
	profile_data.profile_pic_name = "uploaded_images/profilepictures/{}".format(filename)
	profile_data.bio = new_bio
	db.session.commit()
		
	return redirect(url_for('main.profile', identifier = current_user.id))


@main.route('/search', methods = ['GET'])
@login_required
def search_page():
	search = request.args.get('search')
	search = "%{}%".format(search)
	profiles = Profile.query.filter(Profile.name.like(search)).all()

	return render_template('search.html', profiles= profiles)


@main.route('/follow/<profile_id>')
@login_required
def follow_unfollow_button(profile_id):
	if check_follow(profile_id) == False:
		new_follower = Followers(follower=current_user.id, following=profile_id)
		db.session.add(new_follower)
		db.session.commit()
	elif check_follow(profile_id) == True:
		followers_data = Followers.query.filter(Followers.follower == current_user.id, Followers.following == profile_id).all()
		for follower_data in followers_data:
			db.session.delete(follower_data)
		db.session.commit()
	return redirect(url_for('main.profile', identifier = profile_id))





