#Millie & Lubica
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, HiddenField


class FindFriendsForm(FlaskForm):
    username = StringField("Username", render_kw={"class": ""} )
    location = StringField("Location", render_kw={"class": ""})
    age = StringField("Age", render_kw={"class": ""})
    fitness_level = StringField("Fitness Level", render_kw={"class": ""} )
    favourite_exercise = StringField("Favourite Exercise", render_kw={"class": ""})

class AddFriendForm(FlaskForm):
    add_friend = SubmitField("Add friend")
    send_reqest_to_id = StringField('User id')