from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField, FloatField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from email_validator import *

#Millie duplicated Aysin's code for signup
class UserProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[Optional(), EqualTo("password")])
    location = StringField("Location", validators=[DataRequired()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=18, max=150)])
    weight = IntegerField("Weight", validators=[Optional(), NumberRange(min=0)])
    height = FloatField("Height", validators=[Optional(), NumberRange(min=0)])
    fitness_level = SelectField("Fitness Level", 
                                choices=[
                                    ("", "Select Fitness Level"),
                                    ("beginner", "Beginner"),
                                    ("intermediate", "Intermediate"),
                                    ("advanced", "Advanced")
                                ], 
                                validators=[Optional()])
    favourite_exercise = StringField("Favourite Exercise", validators=[Optional()])
    profile_picture = FileField("Upload Profile Picture", 
                                validators=[FileAllowed(["jpg", "png", "jpeg"]) ])    

    submit = SubmitField("Update")