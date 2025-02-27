from flask import Blueprint, render_template

from models.user_point import UserPointModel
from models.user import UserModel
from forms.dashboard_form import DashboardForm
from extension import db

# ----- dashboard route -- | Michal | ------
dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard.route("", methods=['GET', 'POST'])
def dashboard_home():
    form = DashboardForm()
            
    return render_template("dashboard.html", form=form)

@dashboard.route("/friends-leaderboard", methods=['GET', 'POST'])
def friends_leaderboard():
    form = DashboardForm()
    friends_with_points = []
    points_period = "weekly"
    if form.validate_on_submit():
        if form.friends.data:
            points_period = "weekly"
            friends_with_points = ["waiting for friendships model - friends"]
        if form.friends_weekly.data:
            points_period = "weekly"
            friends_with_points = ["waiting for friendships model - friends"]
        elif form.friends_monthly.data:
            points_period = "monthly"
            friends_with_points = ["waiting for friendships model - friends"]
        elif form.friends_yearly.data:
            points_period = "yearly"
            friends_with_points = ["waiting for friendships model - friends"]
        return render_template("dashboard.html", form=form, friends_with_points=friends_with_points, points_period=points_period)
    return render_template("dashboard.html", form=form, friends_with_points=friends_with_points, points_period=points_period)

@dashboard.route('/global-leaderboard', methods=['GET', 'POST'])
def global_leaderboard():
    form = DashboardForm()
    users_with_points = None
    points_period = "weekly"
    # Default weekly points
    users_with_points_weekly = db.session.query(
            UserModel.id, 
            UserModel.username, 
            UserPointModel.weekly_points,
            ).join(UserPointModel, UserPointModel.user_id == UserModel.id).order_by(UserPointModel.weekly_points.desc()).all()
    if form.validate_on_submit():
        if form.all_users.data:
            users_with_points = users_with_points_weekly
        if form.all_users_weekly.data:
            users_with_points = users_with_points_weekly
            points_period = "weekly"
        elif form.all_users_monthly.data:
            users_with_points = db.session.query(
                UserModel.id, 
                UserModel.username, 
                UserPointModel.monthly_points,
                ).join(UserPointModel, UserPointModel.user_id == UserModel.id).order_by(UserPointModel.monthly_points.desc()).all()
            points_period = "monthly"
        elif form.all_users_yearly.data:
            users_with_points = db.session.query(
                UserModel.id, 
                UserModel.username, 
                UserPointModel.yearly_points
                ).join(UserPointModel, UserPointModel.user_id == UserModel.id).order_by(UserPointModel.yearly_points.desc()).all()
            points_period = "yearly"
        return render_template("dashboard.html", form=form, users_with_points=users_with_points, points_period=points_period)
    return render_template("dashboard.html", form=form)