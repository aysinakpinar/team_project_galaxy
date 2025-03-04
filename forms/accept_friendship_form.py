#Michal
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField


class AcceptFriendshipForm(FlaskForm):
    accept_friendship = SubmitField("Accept")
    reject_friendship = SubmitField("Reject")
    friendship_sent_id = HiddenField("Friendship_sent_id")
    friendship_received_id = HiddenField("Friendship_received_id")
