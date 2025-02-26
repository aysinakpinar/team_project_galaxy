from config import TestingConfig 
import os

from extension import db
from flask import Flask
from flask_migrate import Migrate
from models import *
from flask_sqlalchemy import SQLAlchemy

from blueprints.auth import auth



# Create Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(TestingConfig)

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

# Registering blueprints
app.register_blueprint(auth, url_prefix='/auth')



if __name__ == "__main__":
    app.run()