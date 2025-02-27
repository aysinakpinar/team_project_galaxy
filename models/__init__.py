from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models in correct order
from .user import UserModel
from .workout import WorkoutModel
from .exercise import ExerciseModel
from .gym import GymModel