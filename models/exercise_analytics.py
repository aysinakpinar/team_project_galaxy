from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from extension import db

class ExerciseAnalyticsModel(db.Model):
    __tablename__ = "exercise_analytics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_name = db.Column(db.String(200), nullable=True)
    intensity = db.Column(db.String(100), nullable=True)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(100), nullable=True) # None/DONE
    workout_id = db.Column(db.Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exercise_id = db.Column(db.Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)

    workout = db.relationship("WorkoutModel", backref="analytics", lazy=True, cascade="all, delete")