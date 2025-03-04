from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from sqlalchemy import or_, and_
from models.user import UserModel
from extension import db
from forms.find_friends_form import FindFriendsForm
from forms.accept_friendship_form import AcceptFriendshipForm
from models.friendship import FriendshipModel

#The user can search for other users based on their location, age, fitness level and favourite exercise.

friends = Blueprint("friends", __name__, url_prefix="/friends")

@friends.route('/find', methods=['GET', 'POST'])
def find():
    form = FindFriendsForm()

    #shows all users if no search criteria is provided
    query = UserModel.query

    #removed, this option is to show no users as default instead.
    #users = None

    location = request.args.get('location') or form.location.data
    age = request.args.get('age') or form.age.data
    fitness_level = request.args.get('fitness_level') or form.fitness_level.data
    favourite_exercise = request.args.get('favourite_exercise') or form.favourite_exercise.data

    #applies filters only if the values are provided, so can have empty fields.
    if location:
        query = query.filter(UserModel.location.ilike(f"%{location.strip()}%"))
    if age:
        query = query.filter(UserModel.age == age)  # Assuming age is an exact match
    if fitness_level:
        query = query.filter(UserModel.fitness_level.ilike(f"%{fitness_level.strip()}%"))
    if favourite_exercise:
        query = query.filter(UserModel.favourite_exercise.ilike(f"%{favourite_exercise.strip()}%"))

    #if no filter applied, show all users
    users = query.all()

    # ---------- MICHAL - FRIEND REQUESTS -------------------
    form_friendship = AcceptFriendshipForm()
    if form_friendship.validate_on_submit():  # Ensures form is submitted properly
        if form_friendship.reject_friendship.data:
            print("------data-------")
            # print(form_friendship.friendship_received_id.data)
            print(form_friendship.friendship_sent_id.data)
        if form_friendship.accept_friendship.data:
            print(form_friendship.friendship_sent_id.data)
            # print(form_friendship.friendship_received_id.data)
            # print(form_friendship.friendship_id.data)

    approved_friends=get_friends("approved")
    # sent from user
    friendships_sent=get_friends("pending")
    friendships_received=get_pending_received_friendships()
    # print(form_friendship.data)
    if len(approved_friends) == 0:
        approved_friends = [(0, 'no data', 0, 0)]
    if len(friendships_received) == 0:
        friendships_received = [(0, 'no data', 0, 0)]
    if len(friendships_sent) == 0:
        friendships_sent = [(0, 'no data', 0, 0)]
    return render_template("friends.html",form=form, users=users, form_friendship=form_friendship, approved_friends=approved_friends, friendships_sent=friendships_sent, friendships_received=friendships_received)


# ----- | Michal | friend requests --------

# get points sql function
def get_friends(status):
    friends = []
    friends = db.session.query(
        FriendshipModel.user_id,
        UserModel.username,
        UserModel.profile_picture,
        UserModel.id,
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
        UserModel.profile_picture,
        UserModel.id,
        ).join(UserModel, UserModel.id == FriendshipModel.user_id) \
        .filter(and_(
            FriendshipModel.friend_id == session["user_id"],
            FriendshipModel.status == "pending"
        )) \
        .all() 
    print(friendships_received)
    return friendships_received
