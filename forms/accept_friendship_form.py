#Michal
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class AcceptFriendshipForm(FlaskForm):
    cancel_sent_friendship = SubmitField("Cancel")
    accept_received_friendship = SubmitField("Accept")
    reject_received_friendship = SubmitField("Reject")
    friendship_sent_id = StringField("Friendship_sent_id")
    friendship_received_id = StringField("Friendship_received_id")

