from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

class QuoteForm(FlaskForm):
    body = StringField("Body", validators=[DataRequired()])