from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models in correct order
from .user import UserModel
from .user_point import UserPointModel
from .workout import WorkoutModel
from .exercise import ExerciseModel
from .associations import WorkoutExercise
from .gym import GymModel
from .quote import QuoteModel
from .like import LikeModel
from .post import PostModel
from .reply import ReplyModel
