from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from sqlalchemy import or_, and_, not_
from models.user import UserModel
from extension import db
from forms.find_friends_form import FindFriendsForm, AddFriendForm
from forms.accept_friendship_form import AcceptFriendshipForm
from models.friendship import FriendshipModel

#The user can search for other users based on their location, age, fitness level and favourite exercise.

friends = Blueprint("friends", __name__, url_prefix="/friends")

@friends.route('/find', methods=['GET', 'POST'])
def find():
    # ---------- MICHAL - FRIEND REQUESTS -------------------
    form_friendship = AcceptFriendshipForm()
    form_add_friend = AddFriendForm()
    if form_add_friend.validate_on_submit():
        user_to_send_request_id = form_add_friend.send_reqest_to_id.data
        friendship_to_sent_exist = FriendshipModel.query.filter(
            and_(
                FriendshipModel.friend_id == user_to_send_request_id,
                FriendshipModel.user_id == session["user_id"]
            )
        ).first()
        friendship_to_recieve_exist = FriendshipModel.query.filter(
            and_(
                FriendshipModel.user_id == user_to_send_request_id,
                FriendshipModel.friend_id == session["user_id"]
            )
        ).first()

                    
        # if no friendship, add a new friend
        if not friendship_to_sent_exist and not friendship_to_recieve_exist:
            if form_add_friend.send_reqest_to_id.data:
                print("-----------", user_to_send_request_id)
                user_from_request_id = session["user_id"]
                new_friendship = FriendshipModel(user_id=user_from_request_id, friend_id=user_to_send_request_id, status="pending")
                db.session.add(new_friendship)
                db.session.commit()
        # else change the status to pending
        elif(friendship_to_sent_exist):
            friendship_to_sent_exist.status="pending"
            db.session.commit()
        elif(friendship_to_recieve_exist):
            friendship_to_recieve_exist.user_id = session["user_id"]
            friendship_to_recieve_exist.friend_id = user_to_send_request_id 
            friendship_to_recieve_exist.status = "pending"
            db.session.commit()



    
    if form_friendship.validate_on_submit(): 
        action=None
        clicked_id=None
        
        if form_friendship.cancel_sent_friendship.data:
            action="cancel"
            clicked_id = form_friendship.friendship_sent_id.data
            
        if form_friendship.reject_received_friendship.data:
            action="reject"
            clicked_id = form_friendship.friendship_received_id.data
        if form_friendship.accept_received_friendship.data:
            action="accept"
            clicked_id = form_friendship.friendship_received_id.data
        found_friendship = FriendshipModel.query.filter_by(id=clicked_id).first()
        
        if found_friendship and action=="reject":
            found_friendship.status = ""
            db.session.commit()
        if found_friendship and action=="accept":
            found_friendship.status = "approved"
            db.session.commit()
        if found_friendship and action=="cancel":
            found_friendship.status = ""
            db.session.commit()

    approved_friends=get_friends("approved")
    # sent from user
    friendships_sent= []
    friendships_received=[]
    users = []
    friendships_sent = get_pending_friendships_user_is_sender()
    friendships_received = get_pending_friendships_user_is_receiver()
    if len(approved_friends) == 0:
        approved_friends = [(0, 'no data', 0, 0)]
    if len(friendships_received) == 0:
        friendships_received = [(0, 'no data', 0, 0)]
    if len(friendships_sent) == 0:
        friendships_sent = [(0, 'no data', 0, 0)]
    form_find_friend = FindFriendsForm()
 
    #shows all users if no search criteria is provided
    query = UserModel.query

    #removed, this option is to show no users as default instead.
    #users = None

    location = request.args.get('location') or form_find_friend.location.data
    age = request.args.get('age') or form_find_friend.age.data
    fitness_level = request.args.get('fitness_level') or form_find_friend.fitness_level.data
    favourite_exercise = request.args.get('favourite_exercise') or form_find_friend.favourite_exercise.data

    #applies filters only if the values are provided, so can have empty fields.
    if location:
        query = query.filter(UserModel.location.ilike(f"%{location.strip()}%"))
    if age:
        query = query.filter(UserModel.age == age)  # Assuming age is an exact match
    if fitness_level:
        query = query.filter(UserModel.fitness_level.ilike(f"%{fitness_level.strip()}%"))
    if favourite_exercise:
        query = query.filter(UserModel.favourite_exercise.ilike(f"%{favourite_exercise.strip()}%"))

    # ----------- MICHAL - CHANGES --------
    #if no filter applied, show all user which have no frienship connection
    # Ensure users without friendship connection are shown if no filters are applied
    query = query.outerjoin(
        FriendshipModel, or_(
            and_(UserModel.id == FriendshipModel.friend_id, FriendshipModel.user_id == session["user_id"]),
            and_(UserModel.id == FriendshipModel.user_id, FriendshipModel.friend_id == session["user_id"])
        )
    ).filter(
        and_(
            UserModel.id != session["user_id"],
            or_(
                FriendshipModel.id.is_(None),
                not_(FriendshipModel.status.in_(["approved", "pending"]))
            )
        )
    )

    # Fetch the final user list
    users = query.all()
    print("useeeers=----======",users)


    return render_template("friends.html",form_add_friend=form_add_friend,form_find_friend=form_find_friend, users=users, form_friendship=form_friendship, approved_friends=approved_friends, friendships_sent=friendships_sent, friendships_received=friendships_received)


# ----- | Michal | friend requests --------

# get points sql function
def get_friends(status):
    friends = []
    friends = db.session.query(
        FriendshipModel.id,
        UserModel.username,
        UserModel.profile_picture,
        UserModel.id,
        ).join(UserModel, or_(
        and_(UserModel.id == FriendshipModel.friend_id, FriendshipModel.user_id == session["user_id"]),
        and_(UserModel.id == FriendshipModel.user_id, FriendshipModel.friend_id == session["user_id"])
        )).filter(
            FriendshipModel.status == status
        ).all() 
    return friends

def get_pending_friendships_user_is_sender():
    friendships_where_user_is_sender = db.session.query(
        FriendshipModel.id,
        UserModel.username,
        UserModel.profile_picture,
        UserModel.id
    ).join(UserModel, UserModel.id == FriendshipModel.friend_id).filter(
        FriendshipModel.status == "pending",
        FriendshipModel.user_id == session["user_id"]
    ).all()
    return friendships_where_user_is_sender

def get_pending_friendships_user_is_receiver():
    friendships_where_user_is_receiver = db.session.query(
        FriendshipModel.id,
        UserModel.username,
        UserModel.profile_picture,
        UserModel.id
    ).join(UserModel, UserModel.id == FriendshipModel.user_id).filter(
        FriendshipModel.status == "pending",
        FriendshipModel.friend_id == session["user_id"]
    ).all()
    return friendships_where_user_is_receiver