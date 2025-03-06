from extension import db
from datetime import datetime, timezone

class ReplyModel(db.Model):
    __tablename__ = "replies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_Id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    replier_Id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey("replies.id", ondelete="CASCADE"), nullable=True)
    username = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    img = db.Column(db.String(200), nullable=True)
    replied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    parent = db.relationship("ReplyModel", remote_side=[id], backref="replies", cascade="all, delete")

