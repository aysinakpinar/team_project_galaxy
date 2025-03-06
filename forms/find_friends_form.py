#Millie & Lubica
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, HiddenField


class FindFriendsForm(FlaskForm):
    username = StringField("Username")
    location = StringField("Location")
    age = StringField("Age")
    fitness_level = StringField("Fitness Level" )
    favourite_exercise = StringField("Favourite Exercise")

class AddFriendForm(FlaskForm):
    add_friend = SubmitField("Add friend")
    send_reqest_to_id = StringField('User id')