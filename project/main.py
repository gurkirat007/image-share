from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import db
from .models import User, Profile

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

# login required
@main.route('/profile')
@login_required
def profile():
	profile_page_data = Profile.query.get(current_user.id)
	return render_template('profile.html', name = current_user.name, profile_page_data = profile_page_data)


@main.route('/editprofile')
@login_required
def editprofile():
	return render_template('edit_profile.html')



@main.route('/editprofile', methods = ['POST'])
@login_required
def edit_profile():
	# check if the post request has the file part
	if 'file' not in request.files:
		return redirect(url_for('main.profile'))
	file = request.files['file']
	new_bio = request.form.get('bio')
	if file.filename == '':
		return redirect(url_for('main.profile'))
	if file and allowed_file(file.filename):
		file_name = "pp_{}.{}".format(current_user.id, file.filename.rsplit('.', 1)[1].lower())
		filename = secure_filename(file_name)
		file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
	profile_data = Profile.query.get(current_user.id)
	profile_data.profile_pic_name = "uploaded_images/profilepictures/{}".format(filename)
	profile_data.bio = new_bio
	db.session.commit()
		
	return redirect(url_for('main.profile'))


# @main.route('/search', methods = ['POST'])
# @login_required
# def search_page():
# 	search = request.form.get('search')
# 	search = "%{}%".format(search)
# 	profiles = Profile.query.filter(Profile.name.like(search)).all()

# 	return render_template('search.html', profiles= profiles)


