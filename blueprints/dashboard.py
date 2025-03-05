from flask import Blueprint, render_template, session
from sqlalchemy import or_
import plotly.graph_objects as go
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from collections import Counter

from models.user_point import UserPointModel
from models.friendship import FriendshipModel
from models.user import UserModel
from models.exercise_analytics import ExerciseAnalyticsModel
from forms.dashboard_form import DashboardForm
from extension import db

# ----- dashboard route -- | Michal | ------
dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard.route("", methods=['GET', 'POST'])
def dashboard_home():
    form = DashboardForm()
    points_period = "week"

    # default, when the page is open
    friends_with_points = get_friends_points("weekly")
    bar_chart = create_bar_chart()
    pie_chart = create_pie_chart()
    return render_template("dashboard.html", form=form, friends_with_points=friends_with_points, points_period=points_period, bar_chart=bar_chart, pie_chart=pie_chart)

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

def create_pie_chart():
    labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
    values = [4500, 2500, 1053, 500]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    # Get the HTML representation of the figure for embedding in the template
    graph_html = fig.to_html(full_html=False)

    return graph_html

def create_bar_chart():
    data = get_chart_data()
    # Data for the bar chart
    week_days = []
    workout_times = []
    intensity_colours = []
    if data:
        week_days = data["week_days"]
        workout_times = data["estimated_times"]
        intensities = data["intensities"]
        for intensity in intensities:
            if intensity == "High":
                intensity_colours.append("#6a0bff")
            elif intensity == "Medium":
                intensity_colours.append("#a871ff")
            elif intensity == "Low":
                intensity_colours.append("#d1b3ff")
            else:
                intensity_colours.append("gray")

    # Create a Plotly figure
    fig = go.Figure(data=[go.Bar(
        x=week_days,
        y=workout_times,
        marker=dict(color=intensity_colours),
        hoverinfo='x+y'  # Show hover information on bars
    )])

    fig.update_yaxes(range=[0, 120])

    # Customize the layout
    fig.update_layout(
        title="This week workouts",
        xaxis_title="Week days",
        yaxis_title="Time(minutes)",
        template="plotly",
        plot_bgcolor="#e1e1e1",
        paper_bgcolor="#e1e1e1",
        font=dict(color="black"),
    )

    # Get the HTML representation of the figure for embedding in the template
    graph_html = fig.to_html(full_html=False)

    return graph_html

def get_chart_data():
    current_date = datetime.now()

    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_month = current_date.replace(day=1)
    end_of_month = (start_of_month + relativedelta(months=1, days=-1))
    print(start_of_month, end_of_month)

    found_data_this_week = ExerciseAnalyticsModel.query \
        .filter(ExerciseAnalyticsModel.completed_at >= start_of_week,
                ExerciseAnalyticsModel.completed_at <= end_of_week,
                ExerciseAnalyticsModel.user_id == session["user_id"]) \
        .all()
    if found_data_this_week:
        workout_weekly_data = {
            "Mon":{"estimated_time":0, "intensity":[]}, 
            "Tue":{"estimated_time":0, "intensity":[]}, 
            "Wed":{"estimated_time":0, "intensity":[]}, 
            "Thur":{"estimated_time":0, "intensity":[]}, 
            "Fri":{"estimated_time":0, "intensity":[]}, 
            "Sat":{"estimated_time":0, "intensity":[]}, 
            "Sun":{"estimated_time":0, "intensity":[]}
        }
        workout_id = 0
        for exercise in found_data_this_week:
            workout = exercise.workout
            week_day = exercise.completed_at.strftime("%a") 
            workout_weekly_data[week_day]["intensity"].append(exercise.intensity)
            # get a new workout
            if workout_id != workout.id:
                workout_id = workout.id
                estimated_workout_time = int(workout.estimated_time)
                workout_weekly_data[week_day]["estimated_time"] += estimated_workout_time
                
        most_frequent_intensity = {}

        # find the most frequent intensity 
        for day, details in workout_weekly_data.items():
            # if intensity values 
            if details['intensity']:
                # count number of intesities
                intensity_counts = Counter(details['intensity'])
                most_common_intensity = intensity_counts.most_common(1)[0][0]
                most_frequent_intensity[day] = most_common_intensity
            else:
                most_frequent_intensity[day] = None  
            # get most frequent intensity
            workout_weekly_data[day]["intensity"] = most_frequent_intensity[day]

        # create arrays out of dictionaries
        estimated_times = [data['estimated_time'] for data in workout_weekly_data.values()]
        intensities = [data['intensity'] for data in workout_weekly_data.values()]
        week_days = [data for data in workout_weekly_data.keys()]
        return {"estimated_times":estimated_times, "intensities":intensities, "week_days":week_days}


# get points sql function
def get_friends_points(points_period):
    friends_with_points = []
    points_column = getattr(UserPointModel, f"{points_period}_points")
    friends_with_points = db.session.query(
        FriendshipModel.id,
        UserModel.id,
        UserModel.username,
        UserModel.profile_picture,
        points_column
    ).join(UserModel, or_(
        UserModel.id == FriendshipModel.user_id,
        UserModel.id == FriendshipModel.friend_id
    )).outerjoin(UserPointModel, UserPointModel.user_id == UserModel.id) \
    .filter(or_(
        FriendshipModel.user_id == session["user_id"],
        FriendshipModel.friend_id == session["user_id"]
    )) \
    .filter(UserModel.id != session["user_id"]) \
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