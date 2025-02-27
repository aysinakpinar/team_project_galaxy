from flask_sqlalchemy import SQLAlchemy
from extension import db

# Many-to-Many relationship between Users and Exercises
user_exercise = db.Table(
    "user_exercise",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("exercise_id", db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True),
)

# Many-to-Many relationship between Workouts and Exercises
workout_exercise = db.Table(
    "workout_exercise",
    db.Column("workout_id", db.Integer, db.ForeignKey("workouts.id", ondelete="CASCADE"), primary_key=True),
    db.Column("exercise_id", db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True),
)

