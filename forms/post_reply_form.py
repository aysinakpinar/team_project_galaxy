from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    text = TextAreaField("Post Content", validators = [DataRequired()])
    img = StringField("Image URL", validators = [Length(max=200)])
    submit = SubmitField("Post")

class ReplyForm(FlaskForm):
    text = TextAreaField("Reply Content", validators = [DataRequired()])
    img = StringField("Image URL", validators = [Length(max=200)])
    submit = SubmitField("Reply")
