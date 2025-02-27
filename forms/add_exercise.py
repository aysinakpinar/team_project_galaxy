# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, IntegerField,
# from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
# from email_validator import *

# #Aysin's code for signup
# class AddExercise(FlaskForm):
#     name = StringField("Name", validators=[DataRequired(), Length(min=3, max=20)])
#     description = StringField("Location", validators=[DataRequired()])
#     age = IntegerField("Age", validators=[Optional(), NumberRange(min=18, max=150)])
#     weight = IntegerField("Weight", validators=[Optional(), NumberRange(min=0)])
#     height = IntegerField("Height", validators=[Optional(), NumberRange(min=0)])
#     fitness_level = StringField("Fitness Level", validators=[Optional()])
#     favorite_exercise = StringField("Favorite Exercise", validators=[Optional()])
    

#     submit = SubmitField("Sign Up")