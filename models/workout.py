from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from extension import db
from models.associations import workout_exercise

class WorkoutModel(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    estimated_time = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Many-to-Many Relationship with Exercises
    exercises = db.relationship(
        "ExerciseModel", 
        secondary=workout_exercise, 
        lazy="subquery",
        back_populates="workouts"  # Changed from backref to back_populates
    )
        

    @property
    def list_of_exercises(self):
        """Returns a list of exercise names in the workout."""
        return [exercise.name for exercise in self.exercises]
