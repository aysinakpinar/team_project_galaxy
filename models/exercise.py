# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import backref
# from sqlalchemy.engine import TupleResult
# from datetime import datetime
# from extension import db

# class ExerciseModel(db.Model):
#     __tablename__ = "exercises"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(200), nullable=False, unique=True)
#     description = Column(String(200), nullable=False)
#     intensity = Column(String(200), nullable=True)
#     duration = Column(String(200), nullable=True)
#     picture_path = Column(String(200), nullable=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
#     workout_id = Column(Integer, ForeignKey("workouts.id", ondelete = "CASCADE"), nullable = False)
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now)