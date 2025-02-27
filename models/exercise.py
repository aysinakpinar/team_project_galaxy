from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from extension import db
from models.associations import user_exercise, workout_exercise

class ExerciseModel(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    intensity = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    picture_path = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    done = db.Column(db.Boolean, default=False, nullable=False)

    # Many-to-Many Relationships
    users = db.relationship(
        "UserModel", 
        secondary=user_exercise, 
        back_populates="exercises"
        )
    
    workouts = db.relationship(
        "WorkoutModel", 
        secondary=workout_exercise, 
        back_populates="exercises")
