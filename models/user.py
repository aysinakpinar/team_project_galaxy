from datetime import datetime, timezone
from extension import db
from models.associations import user_exercise
from models.friendship import FriendshipModel
from models.post import PostModel
from models.reply import ReplyModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
<<<<<<< HEAD
    fitness_level = db.Column(db.String(200), nullable=True)
    favorite_exercise = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

=======
    fitness_level = db.Column(db.String(200), nullable=True)  
    favorite_exercise = db.Column(db.String(200), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.now)  
>>>>>>> 8e12fda66f7b3ae631d8fcd3465c717e43c9cce6

    # Relationships
    workouts = db.relationship(
        "WorkoutModel", 
        backref="user", 
        lazy=True, 
        cascade="all, delete"
    )
    gyms = db.relationship(
        "GymModel", 
        backref="user", 
        lazy=True, 
        cascade="all, delete"
    )
    # Many-to-Many with Exercises
    exercises = db.relationship(
        "ExerciseModel", 
        secondary=user_exercise, 
        back_populates="users"
    )

    posts = db.relationship(
        "PostModel",
        backref="poster",
        lazy=True,
        cascade="all, delete"
    )

    replies = db.relationship(
        "ReplyModel",
        backref="replier",
        lazy=True,
        cascade="all, delete"
    )


    def add_friend(self, friend):
        """Creates a friendship between two users."""
        if not FriendshipModel.query.filter_by(user_id=self.id, friend_id=friend.id).first():
            friendship = FriendshipModel(user_id=self.id, friend_id=friend.id)
            db.session.add(friendship)
            db.session.commit()

