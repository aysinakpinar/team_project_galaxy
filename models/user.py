from sqlalchemy.orm import backref
from sqlalchemy.engine import TupleResult
from datetime import datetime, timezone
from extension import db

#Aysin's code for user model
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
    fitness_level = db.Column(db.String(200), nullable=True)  
    favorite_exercise = db.Column(db.String(200), nullable=True)  
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc)) 

    # Relationships
    # exercises = db.relationship("ExerciseModel", backref="user", lazy=True, cascade="all, delete")
    # workouts = db.relationship("WorkoutModel", backref="user", lazy=True, cascade="all, delete")
    # friendships = db.relationship("FriendshipModel", backref="user", lazy=True, cascade="all, delete")