from extension import db

class FriendshipModel(db.Model):
    __tablename__ = "friendships"

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Optional timestamp

    #relationships
    user = db.relationship(
        "UserModel", 
        foreign_keys=[user_id], 
        backref="friendships_sent"
    )
    friend = db.relationship(
        "UserModel", 
        foreign_keys=[friend_id], 
        backref="friendships_received"
    )
    def __repr__(self):
        return f"<Friendship {self.user_id} - {self.friend_id}>"
