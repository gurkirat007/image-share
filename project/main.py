from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import User, Profile

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# login required
@main.route('/profile')
@login_required
def profile():
	profile_page_data = Profile.query.get(current_user.id)
	return render_template('profile.html', name = current_user.name, profile_page_data = profile_page_data)


# @main.route('/profile')
# @login_required
# def edit_profile():