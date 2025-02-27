#Millie & Lubica
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField


class FindFriendsForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    #favourite exercise.