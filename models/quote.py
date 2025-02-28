from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from extension import db
from sqlalchemy.engine import TupleResult

class QuoteModel(db.Model):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String(255), nullable=False, unique=True)
