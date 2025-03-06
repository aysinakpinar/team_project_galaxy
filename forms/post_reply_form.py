from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    text = TextAreaField("Post Content", validators = [DataRequired()])
    img = FileField('image')
    submit = SubmitField("Post")

class ReplyForm(FlaskForm):
    text = TextAreaField("Reply Content", validators = [DataRequired()])
    img = FileField('image')
    submit = SubmitField("Reply")
