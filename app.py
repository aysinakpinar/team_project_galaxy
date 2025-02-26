from extension import db
from flask import Flask
from flask_migrate import Migrate
from models import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from blueprints.auth import auth

def create_app(config_class=None):
    #create and configure the Flask App
    app = Flask(__name__)

    if config_class is None:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    else:
        app.config.from_object(config_class)

    if "SQLALCHEMY_DATABASE_URI" not in app.config:
        raise RuntimeError("❌ SQLALCHEMY_DATABASE_URI is missing from config.py!")

    db.init_app(app)  # Initialize the SQLAlchemy instance with the Flask app
    migrate = Migrate(app, db)  # Create a Migrate instance for database migrations

    app.register_blueprint(auth)

    return app

if __name__ == "__main__":
    app = create_app()

    # Test database connection
    try:
        with app.app_context():  # Ensure the code runs within the Flask application context
            with db.engine.connect() as connection:  # Establish a connection to the database
                print("PostgreSQL connection successful!")
    except Exception as e:
        print("Failed to connect to PostgreSQL:", str(e))  # Print the error message if connection fails

    app.run()



