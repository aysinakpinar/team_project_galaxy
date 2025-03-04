from extension import db

class LikeModel(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    reply_id = db.Column(db.Integer, db.ForeignKey('replies.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('UserModel', backref='likes')
    post = db.relationship('PostModel', backref='likes')
    reply = db.relationship('ReplyModel', backref='likes')

    # Ensure a like is either for a post or a reply, not both or neither
    __table_args__ = (
        db.CheckConstraint(
            '(post_id IS NOT NULL AND reply_id IS NULL) OR '
            '(post_id IS NULL AND reply_id IS NOT NULL)',
            name='check_content_type'
        ),
    )