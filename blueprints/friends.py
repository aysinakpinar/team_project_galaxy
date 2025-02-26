#from crypt import methods

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from sqlalchemy.sql.operators import from_
from wtforms.validators import email

from forms.friends_form import FindFriendForm
#from forms.login_form import LoginForm
#from forms.register_form import RegisterForm
from models import UserModel
from extension import db
#from forms import register_form, login_form
from werkzeug.security import generate_password_hash, check_password_hash

friends = Blueprint("friends", __name__, url_prefix= "/friends")

@friends.route('/friends', methods=['GET'])
def suggest_friends():
    print("Hi")
    # form = FindFriendForm()
    # friends = UserModel.query.filter(UserModel.location == form.location, UserModel.username != form.username).all()
    # if not friends:
    #     return "No friends found in the location."
    return render_template("friends.html")