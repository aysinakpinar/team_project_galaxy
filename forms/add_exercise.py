from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class AddExerciseForm(FlaskForm):
    name = SelectField("Exercise Name", choices=[], validators=[DataRequired()])
    submit = SubmitField("Add Exercise")

