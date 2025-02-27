#Millie & Lubica
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField


class FindFriendsForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    #submit = SubmitField("Search")
    #favourite exercise.