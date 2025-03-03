#Michal
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class AcceptFriendshipForm(FlaskForm):
    accept_friendship = SubmitField("Accept")
    reject_friendship = SubmitField("Reject")
    friendship_id = StringField("Friend_id")
