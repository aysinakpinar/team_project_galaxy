from flask_wtf import FlaskForm
from wtforms import SubmitField


# Dashboard form - | Michal |
class DashboardForm(FlaskForm):
    friends = SubmitField('friends')
    friends_weekly = SubmitField('week')
    friends_monthly = SubmitField('month')
    friends_yearly = SubmitField('year')
    all_users = SubmitField('global')
    all_users_weekly = SubmitField('week')
    all_users_monthly = SubmitField('month')
    all_users_yearly = SubmitField('year')