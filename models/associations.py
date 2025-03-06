from flask_sqlalchemy import SQLAlchemy
from extension import db

# ✅ Many-to-Many Relationship between Users and Exercises
user_exercise = db.Table(
    "user_exercise",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("exercise_id", db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True),
)

# ✅ WorkoutExercise Model (Not just a table)
class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercise"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    done = db.Column(db.Boolean, default=False)

    # Use string names to avoid circular import issues
    workout = db.relationship("WorkoutModel", back_populates="workout_exercises")
    exercise = db.relationship("ExerciseModel", back_populates="exercise_workouts")

    analytics_ref = db.relationship("ExerciseAnalyticsModel", backref="workout_exercise", lazy=True, cascade="all, delete")

