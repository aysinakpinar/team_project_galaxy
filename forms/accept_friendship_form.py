#Michal
from flask_wtf import FlaskForm
from wtforms import SubmitField


class AcceptFriendshipForm(FlaskForm):
    accept_friendship = SubmitField("Accept")
    reject_friendship = SubmitField("Reject")
