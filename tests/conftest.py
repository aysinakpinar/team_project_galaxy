import sys
import os
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extension import db
from models.user import UserModel
from models.friendship import FriendshipModel
from models.user_point import UserPointModel
from dotenv import load_dotenv
from config import TestingConfig

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def app():
    """Create a Flask test application."""
    from app import create_app

    # using TestingConfig for tests
    app = create_app(config_class=TestingConfig)
    
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

# create_user fixture -- | Michal |
@pytest.fixture
def create_user(database):
    """Fixture to add a user to the database."""
    def _create_user( username, password, email, location):
        user = UserModel(
            id=None,
            username=username,
            password=password,
            email=email,
            location=location
        )
        database.session.add(user)
        database.session.commit()
        return user  # Return the user instance
    return _create_user  

@pytest.fixture
def create_friendship(database):
    """Fixture to add a friendship to the database."""
    def _create_friendship(user_id, friend_id):
        friendship = FriendshipModel(
            id=None,
            user_id=user_id,
            friend_id=friend_id
        )
        database.session.add(friendship)
        database.session.commit()
        return friendship
    return _create_friendship

@pytest.fixture
def create_user_point(database):
    """Fixture to add a user point to the database."""
    def _create_user_point(weekly_points, monthly_points, yearly_points, user_id):
        # Create a user instance
        user_point = UserPointModel(
            id=None,
            weekly_points=weekly_points,
            monthly_points=monthly_points,
            yearly_points=yearly_points,
            user_id=user_id
        )
        database.session.add(user_point)
        database.session.commit()
        return user_point
    return _create_user_point
