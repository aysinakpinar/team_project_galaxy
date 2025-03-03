from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from extension import db
from sqlalchemy.engine import TupleResult

class QuoteModel(db.Model):
    __tablename__ = "quotes"
    
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Quote {self.body}>"
