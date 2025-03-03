from flask import Blueprint, render_template, session
from sqlalchemy import or_, and_

from models.user_point import UserPointModel
from models.friendship import FriendshipModel
from models.user import UserModel
from forms.accept_friendship_form import AcceptFriendshipForm
from extension import db

# ----- dashboard route -- | Michal | ------
user_profile = Blueprint("user-profile", __name__, url_prefix="/user-profile")

# get points sql function
def get_friends(status):
    friends = []
    friends = db.session.query(
        FriendshipModel.friend_id,
        UserModel.username,
        ).join(UserModel, UserModel.id == FriendshipModel.friend_id) \
        .filter(and_(
            FriendshipModel.user_id == session["user_id"],
            FriendshipModel.status == status
        )) \
        .all()  
    if len(friends) == 0:
        friends = [(0, 'no data', 0)]
    return friends

@user_profile.route("", methods=['GET', 'POST'])
def display_friends():
    form = AcceptFriendshipForm()
    approved_friends=get_friends("approved")
    pending_friends=get_friends("pending")
    print(form.data)
    return render_template("user_profile.html", form=form, approved_friends=approved_friends, pending_friends=pending_friends)