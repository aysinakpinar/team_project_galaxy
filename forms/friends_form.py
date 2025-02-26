from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from email_validator import *

class FindFriendForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    location = StringField("Location", validators=[DataRequired()])
