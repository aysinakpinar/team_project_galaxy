from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from models.user import UserModel
from extension import db
from forms.find_friends_form import FindFriendsForm

#Searching users based on their location 
#Millie & Lubica

friends = Blueprint("friends", __name__, url_prefix="/friends")

@friends.route('/find', methods=['GET', 'POST'])
def find():
    form = FindFriendsForm()
    users = None
    location = request.args.get('location') or form.location.data

    if location:
        location = location.strip()
        users = UserModel.query.filter(UserModel.location.ilike(f"%{location}%")).all()
    
    return render_template("friends.html", form=form, users=users)
