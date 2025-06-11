from config import DevelopmentConfig
from extension import db
from flask import Flask
from flask_migrate import Migrate
import os

from models.user import UserModel
from models.workout import WorkoutModel
from models.exercise import ExerciseModel
from models.friendship import FriendshipModel
from models.post import PostModel
from models.reply import ReplyModel
from models.gym import GymModel
from models.associations import *

from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO # Importing Socketio for real time communications
# initialise socketio globally
socketio = SocketIO(cors_allowed_origins="*") #allows all domains to connect using socketio

def create_app(config_class=None):
    #create and configure the Flask App
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object(DevelopmentConfig)

    if "SQLALCHEMY_DATABASE_URI" not in app.config:
        raise RuntimeError("❌ SQLALCHEMY_DATABASE_URI is missing from config.py!")

    # Initialize extensions
    db.init_app(app)  # Initialize the SQLAlchemy instance with the Flask app
    migrate = Migrate(app, db)  # Create a Migrate instance for database migrations

    # Test database connection
    try:
        with app.app_context():  # Ensure the code runs within the Flask application context
            with db.engine.connect() as connection:  # Establish a connection to the database
                print("PostgreSQL connection successful!")
    except Exception as e:
        print("Failed to connect to PostgreSQL:", str(e))  # Print the error message if connection fails
    
    from blueprints.auth import auth
    from blueprints.dashboard import dashboard
    from blueprints.friends import friends
    from blueprints.gym_search import gym_search
    from blueprints.users import users
    from blueprints.threads import threads
    from blueprints.workout import workout
    from blueprints.home import home
    from blueprints.chatbot import chatbot
    from blueprints.chat import chat, init_socketio

    # Registering blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/dashboard') #register user route
    app.register_blueprint(friends)
    app.register_blueprint(gym_search)
    app.register_blueprint(users)
    app.register_blueprint(threads, url_prefix='/threads')
    app.register_blueprint(home)
    app.register_blueprint(workout, url_prefix='/workout')
    app.register_blueprint(chatbot, url_prefix='/chatbot')

    #khadijas chat code
    app.register_blueprint(chat, url_prefix='/chat')
    socketio.init_app(app) #initialise socketio w app
    init_socketio(socketio) #initialises socketio event handlers


    return app

if __name__ == "__main__":
    app = create_app()


#khadijas chat code
    socketio.run(app, debug=True) #start app using socketio server