import sys
import os
import pytest
from unittest.mock import MagicMock

# Add the project root to sys.path to ensure correct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary components
from extension import db
from models.user import UserModel
from models.friendship import FriendshipModel
from models.user_point import UserPointModel
from config import TestingConfig

# =============================================================================
# CORE TEST FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def monkeypatch_session():
    """
    A session-scoped monkeypatch to allow patching for the whole test session.
    This runs before anything else that depends on it.
    """
    from _pytest.monkeypatch import MonkeyPatch
    m = MonkeyPatch()
    yield m
    m.undo()

@pytest.fixture(scope="session")
def app(monkeypatch_session):
    """
    Creates the Flask test application.
    
    This fixture now depends on `monkeypatch_session` to guarantee that the
    googlemaps.Client is mocked BEFORE the app factory is called.
    """
    # STEP 1: Patch the googlemaps.Client class globally. This happens first.
    monkeypatch_session.setattr("googlemaps.Client", MagicMock())
    
    # STEP 2: Now that the patch is active, it's safe to import and create the app.
    from app import create_app
    app = create_app(config_class=TestingConfig)
    
    # if there is an env var, override
    if os.getenv('TEST_DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')

    return app

@pytest.fixture(scope="function")
def client(app):
    """A test client for the app, created for each test function."""
    return app.test_client()

@pytest.fixture(scope="function")
def database(app):
    """Creates a new, clean database for each test function."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

# =============================================================================
# MODEL FACTORY FIXTURES (for creating test data)
# =============================================================================

@pytest.fixture
def create_user(database):
    """Fixture to add a user to the database."""
    def _create_user(username, password, email, location):
        user = UserModel(
            id=None,
            username=username,
            password=password,
            email=email,
            location=location
        )
        database.session.add(user)
        database.session.commit()
        return user
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

# NOTE: The old `mock_gmaps_client` fixture has been removed as its logic is now
# correctly placed inside the `app` fixture to control the order of operations.