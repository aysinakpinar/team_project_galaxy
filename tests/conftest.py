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
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = TestingConfig
    
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

# # create_user fixture -- | Michal |
@pytest.fixture
def create_user(database):
    """Fixture to add a user to the database."""
    # Create a user instance
    test_user = UserModel(
        id=1,
        username='test_user',
        password="Test12345!", 
        email="test@email.com",
        location="test_location"
    )
    database.session.add(test_user)
    database.session.commit()
    yield test_user

# @pytest.fixture
# def create_some_users(database):
#     """Fixture to add a user to the database."""
#     # Create a user instance
#     test_user_1 = UserModel(
#         id=1,
#         username='test_user_1',
#         password="Test12345!", 
#         email="test_1@email.com",
#         location="test_location_1"
#     )
#     test_user_2 = UserModel(
#         id=2,
#         username='test_user_2',
#         password="Test12345!", 
#         email="test_2@email.com",
#         location="test_location_2"
#     )
#     test_user_3 = UserModel(
#         id=3,
#         username='test_user_3',
#         password="Test12345!", 
#         email="test_3@email.com",
#         location="test_location_3"
#     )
#     database.session.add(test_user_1)
#     database.session.add(test_user_2)
#     database.session.add(test_user_3)
#     database.session.commit()
#     yield test_user_1
#     yield test_user_2
#     yield test_user_3

# @pytest.fixture
# def create_some_friendships(database):
#     """Fixture to add a user to the database."""
#     # Create a user instance
#     test_friendship_1 = FriendshipModel(
#         id=1,
#         user_id=1,
#         friend_id=2
#     )
#     test_friendship_2 = FriendshipModel(
#         id=2,
#         user_id=1,
#         friend_id=3
#     )
#     database.session.add(test_friendship_1)
#     database.session.add(test_friendship_2)
#     database.session.commit()
#     yield test_friendship_1
#     yield test_friendship_2

# @pytest.fixture
# def create_some_user_points(database):
#     """Fixture to add a user to the database."""
#     # Create a user instance
#     user_points_1 = UserPointModel(
#         id=1,
#         weekly_points=15,
#         monthly_points=50,
#         yearly_points=400,
#         user_id=1
#     )
#     user_points_2 = UserPointModel(
#         id=2,
#         weekly_points=25,
#         monthly_points=70,
#         yearly_points=500,
#         user_id=2
#     )
#     user_points_3 = UserPointModel(
#         id=3,
#         weekly_points=35,
#         monthly_points=90,
#         yearly_points=600,
#         user_id=3
#     )
#     database.session.add(user_points_1)
#     database.session.add(user_points_2)
#     database.session.add(user_points_3)
#     database.session.commit()
#     yield user_points_1 
#     yield user_points_2
#     yield user_points_3