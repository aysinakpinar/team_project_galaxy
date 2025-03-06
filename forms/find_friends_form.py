#Millie & Lubica
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, HiddenField


class FindFriendsForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    age = StringField("Age", validators=[DataRequired()])
    fitness_level = StringField("Fitness Level", validators=[DataRequired()])
    favourite_exercise = StringField("Favourite Exercise", validators=[DataRequired()])

class AddFriendForm(FlaskForm):
    add_friend = SubmitField("Add friend")
    send_reqest_to_id = StringField('User id')