import sys
import os
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extension import db
from models.user import UserModel
from dotenv import load_dotenv
from config import TestingConfig

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def app():
    """Create a Flask test application."""
    from app import create_app

    # using TestingConfig for tests
    app = create_app(TestingConfig)

    # if there is an env var, override
    if os.getenv('TEST_DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')

    return app

@pytest.fixture(scope="function")
def database(app):
    """Create a new database for each test function."""
    with app.app_context():
        db.create_all()  # Ensure tables are created
        yield db
        db.session.remove()
        db.drop_all()  # Clean up after test
