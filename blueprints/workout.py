from flask import Blueprint

workout = Blueprint('exercises', __name__, url_prefix='/workout')

##@exercises.route('/')