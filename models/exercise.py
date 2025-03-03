from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from extension import db
from models.associations import user_exercise, WorkoutExercise
 

class IntensityEnum(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ExerciseModel(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    intensity = db.Column(Enum("Low", "Medium", "High", name="intensity_enum"), nullable=True)  # ✅ Enum
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    picture_path = db.Column(db.String(200), nullable=True, default=None)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Many-to-Many Relationships
    users = db.relationship(
        "UserModel", 
        secondary="user_exercise",  # ✅ Kept this Many-to-Many
        lazy="subquery", 
        back_populates="exercises"
    )

    # Relationship with WorkoutExercise (Tracks Done ✅)
    exercise_workouts = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")