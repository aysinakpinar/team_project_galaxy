from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, ValidationError
from wtforms.validators import DataRequired, Email


# Login form - | Michal |
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

