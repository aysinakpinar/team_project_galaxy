from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from models.quote import QuoteModel
from extension import db
from datetime import datetime
import random

quote = Blueprint("home", __name__, url_prefix="/home")

@quote.route('/quote', methods=['GET'])
def quote_of_day():
    quotes = db.session.query(QuoteModel).all()
    print("hi")
    print(quotes)
    quote = random.choice(quotes)
    return render_template("home.html", quote=quote)