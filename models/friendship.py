from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import backref
from sqlalchemy.engine import TupleResult
from datetime import datetime
from extension import db

class FriendshipModel(db.Model):
    __tablename__ = "friendships"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)

