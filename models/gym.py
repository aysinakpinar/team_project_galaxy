from decimal import Decimal
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import backref
from sqlalchemy.engine import TupleResult
from datetime import datetime
from extension import db


class GymModel(db.Model):
    __tablename__ = "gyms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    picture_path = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    location = db.Column(db.String(200), nullable=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

def __repr__(self):
    return f"<Gym {self.name}>"