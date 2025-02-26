# from sqlalchemy.orm import backref
# from sqlalchemy.engine import TupleResult
# from datetime import datetime
# from extension import db

# class WorkoutModel(db.Model):
#     __tablename__ = "workouts"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(200), nullable=False, unique=True)
#     list_of_exercises = db.Column(db.String(200), nullable=False)
#     estimated_time = db.Column(db.String(200), nullable=False) 
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)  

#     # Relationships
#     exercises = db.relationship("ExerciseModel", backref="workout", lazy=True, cascade="all, delete")
#     users = db.relationship("UserModel", backref="workout", lazy=True, cascade="all, delete")
