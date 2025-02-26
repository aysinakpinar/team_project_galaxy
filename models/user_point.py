from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import backref
from sqlalchemy.engine import TupleResult
from datetime import datetime
from extension import db

class UserPointsModel(db.Model):
    __tablename__ = "user_points"
    id = Column(Integer, primary_key=True, autoincrement=True)
    weekly_points = Column(Integer, nullable=False)
    monthly_points = Column(Integer, nullable=False)
    yearly_points = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)