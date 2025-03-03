from flask import Blueprint, render_template, session
from sqlalchemy import or_, and_

from models.user_point import UserPointModel
from models.friendship import FriendshipModel
from models.user import UserModel
from forms.accept_friendship_form import AcceptFriendshipForm
from extension import db

# ----- dashboard route -- | Michal | ------
friend_zone = Blueprint("friend-zone", __name__, url_prefix="/friend-zone")

# get points sql function
def get_friends(status):
    friends = []
    friends = db.session.query(
        FriendshipModel.id,
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

def get_pending_received_friendships():
    friendships_received = db.session.query(
        FriendshipModel.id,
        UserModel.username,
        ).join(UserModel, UserModel.id == FriendshipModel.user_id) \
        .filter(and_(
            FriendshipModel.friend_id == session["user_id"],
            FriendshipModel.status == "pending"
        )) \
        .all() 
    print(friendships_received)
    return friendships_received

@friend_zone.route("", methods=['GET', 'POST'])
def display_friends():
    form = AcceptFriendshipForm()
    approved_friends=get_friends("approved")
    # sent from user
    friendships_sent=get_friends("pending")
    friendships_received=get_pending_received_friendships()
    print(form.data)
    return render_template("friend_zone.html", form=form, approved_friends=approved_friends, friendships_sent=friendships_sent, friendships_received=friendships_received)