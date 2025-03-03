from datetime import datetime, timezone
from extension import db
from models.associations import user_exercise
from models.friendship import FriendshipModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)
    fitness_level = db.Column(db.String(200), nullable=True)
    favourite_exercise = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


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
    def add_friend(self, friend):
        """Creates a friendship between two users."""
        if not FriendshipModel.query.filter_by(user_id=self.id, friend_id=friend.id).first():
            friendship = FriendshipModel(user_id=self.id, friend_id=friend.id)
            db.session.add(friendship)
            db.session.commit()

