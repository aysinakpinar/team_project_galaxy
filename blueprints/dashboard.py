from flask import Blueprint, render_template

from models.user_point import UserPointsModel
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
    if form.validate_on_submit():
        if form.friends_weekly.data:
            weekly_leaderboard = ["waiting for friendships model - friends"]
        elif form.all_users.data:
            # found_user = UserModel.query.filter_by(email=submitted_email).first()
            weekly_leaderboard = UserPointsModel.query.order_by(UserPointsModel.weekly_points.desc()).all()
            monthly_leaderboard = UserPointsModel.query.order_by(UserPointsModel.monthly_points.desc()).all()
            yearly_leaderboard = UserPointsModel.query.order_by(UserPointsModel.yearly_points.desc()).all()
        # # Create a list to store the results (user id and username)
        # leaderboard_with_usernames = []

        # # Loop through the leaderboard and get the corresponding user names
        # for user_points in weekly_leaderboard:
        #     user_id = user_points.id  # Get the user id from UserPointsModel
            
        #     # Query the UserModel to get the username corresponding to the user_id
        #     user = UserModel.query.filter_by(id=user_id).first()
            
        #     if user:
        #         # Append a tuple of the points and the username
        #         leaderboard_with_usernames.append({
        #             'user_id': user.id,
        #             'username': user.username,
        #             'weekly_points': user_points.weekly_points
        #         })
        return render_template("dashboard.html", form=form, leaderboard=weekly_leaderboard)
    return render_template("dashboard.html", form=form)

@dashboard.route('/global-leaderboard', methods=['GET', 'POST'])
def global_leaderboard():
    form = DashboardForm()
    if form.validate_on_submit():
        if form.all_users_weekly.data:
            weekly_leaderboard = ["waiting for friendships model - users"]
        elif form.all_users.data:
            # found_user = UserModel.query.filter_by(email=submitted_email).first()
            weekly_leaderboard = UserPointsModel.query.order_by(UserPointsModel.weekly_points.desc()).all()
            monthly_leaderboard = UserPointsModel.query.order_by(UserPointsModel.monthly_points.desc()).all()
            yearly_leaderboard = UserPointsModel.query.order_by(UserPointsModel.yearly_points.desc()).all()
        # # Create a list to store the results (user id and username)
        # leaderboard_with_usernames = []

        # # Loop through the leaderboard and get the corresponding user names
        # for user_points in weekly_leaderboard:
        #     user_id = user_points.id  # Get the user id from UserPointsModel
            
        #     # Query the UserModel to get the username corresponding to the user_id
        #     user = UserModel.query.filter_by(id=user_id).first()
            
        #     if user:
        #         # Append a tuple of the points and the username
        #         leaderboard_with_usernames.append({
        #             'user_id': user.id,
        #             'username': user.username,
        #             'weekly_points': user_points.weekly_points
        #         })
        return render_template("dashboard.html", form=form, leaderboard=weekly_leaderboard)
    return render_template("dashboard.html", form=form)