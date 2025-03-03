from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from email_validator import *

#Aysin's code for signup
class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    location = StringField("Location", validators=[DataRequired()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=18, max=150)])
    weight = IntegerField("Weight", validators=[Optional(), NumberRange(min=0)])
    height = IntegerField("Height", validators=[Optional(), NumberRange(min=0)])
    fitness_level = StringField("Fitness Level", validators=[Optional()])
    favourite_exercise = StringField("Favourite Exercise", validators=[Optional()])
    

    submit = SubmitField("Sign Up")