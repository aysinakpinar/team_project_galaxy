from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    text = TextAreaField(
        "Post Content",
        validators = [DataRequired()],
        render_kw={
            "class": "form-control post-textarea",
            "placeholder": "What's on your mind?",
            "rows": "5",
            "style": "width: 100%; max-width: 600px;"
        })
    img = FileField('image')
    submit = SubmitField("Post")

class ReplyForm(FlaskForm):
    text = TextAreaField("Reply Content", validators = [DataRequired()])
    img = FileField('image')
    submit = SubmitField("Reply")
