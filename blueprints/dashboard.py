from flask import Blueprint, render_template, session
from sqlalchemy import or_

from models.user_point import UserPointModel
from models.friendship import FriendshipModel
from models.user import UserModel
from forms.dashboard_form import DashboardForm
from extension import db

# ----- dashboard route -- | Michal | ------
dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# get points sql function
def get_friends_points(points_period):
    friends_with_points = []
    points_column = getattr(UserPointModel, f"{points_period}_points")
    friends_with_points = db.session.query(
        FriendshipModel.friend_id,
        UserModel.username,
        points_column,
        UserModel.profile_picture
        ).join(UserPointModel, UserPointModel.user_id == FriendshipModel.friend_id) \
        .join(UserModel, UserModel.id == UserPointModel.user_id) \
        .filter(or_(
            FriendshipModel.user_id == session["user_id"],
        )) \
        .order_by(points_column.desc()) \
        .all()  
    if len(friends_with_points) == 0:
        friends_with_points = [(0, 'no data', 0)]
    return friends_with_points

# get points sql function
def get_users_points(points_period):
    users_with_points = []
    points_column = getattr(UserPointModel, f"{points_period}_points")
    users_with_points = db.session.query(
            UserModel.id, 
            UserModel.username, 
            points_column,
            UserModel.profile_picture
            ).join(UserPointModel, UserPointModel.user_id == UserModel.id) \
            .order_by(points_column.desc()).all()
    if len(users_with_points) == 0:
        users_with_points = [(0, 'no data', 0)]
    return users_with_points

@dashboard.route("", methods=['GET', 'POST'])
def dashboard_home():
    form = DashboardForm()
    points_period = "week"

    # default, when the page is open
    friends_with_points = get_friends_points("weekly")
    return render_template("dashboard.html", form=form, friends_with_points=friends_with_points, points_period=points_period)

@dashboard.route("/friends-leaderboard", methods=['GET', 'POST'])
def friends_leaderboard():
    form = DashboardForm()
    # default, when the page is open
    points_period = "week"
    friends_with_points = get_friends_points("weekly")
    if form.validate_on_submit():
        if form.friends.data:
            points_period = "week"
            friends_with_points = get_friends_points("weekly")
        if form.friends_weekly.data:
            points_period = "week"
            friends_with_points = get_friends_points("weekly")
        elif form.friends_monthly.data:
            points_period = "month"
            friends_with_points = get_friends_points("monthly")
        elif form.friends_yearly.data:
            points_period = "year"
            friends_with_points = get_friends_points("yearly")
        return render_template("dashboard.html", form=form, friends_with_points=friends_with_points, points_period=points_period)
    return render_template("dashboard.html", form=form, friends_with_points=friends_with_points, points_period=points_period)

@dashboard.route('/global-leaderboard', methods=['GET', 'POST'])
def global_leaderboard():
    form = DashboardForm()
    points_period = "week"
    users_with_points = get_users_points("weekly")

    if form.validate_on_submit():
        # if clicked on global
        if form.all_users.data:
            points_period = "week"
            users_with_points = get_users_points("weekly")
        # if clicked on weekly users leaderboard
        if form.all_users_weekly.data:
            points_period = "week"
            users_with_points = get_users_points("weekly")
        # if clicked on monthly users leaderboard
        elif form.all_users_monthly.data:
            points_period = "month"
            users_with_points = get_users_points("monthly")
        # if clicked on yearly users leaderboard
        elif form.all_users_yearly.data:
            points_period = "year"
            users_with_points = get_users_points("yearly")
        return render_template("dashboard.html", form=form, users_with_points=users_with_points, points_period=points_period)
    return render_template("dashboard.html", form=form, users_with_points=users_with_points, points_period=points_period)

