import pytest
from models.user import *
from models import UserModel
from flask import *
from extension import db
from app import create_app
from tests.factories import create_user
# Khadija, Millie & Louis logout test code 
# create dummy user to log out

@pytest.fixture(scope="function")
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            user = UserModel(
                id=1,
                username="jack",
                email="jack@email.com",
                password="password",
                location="London"
            )
            db.session.add(user)

        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_logout(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/auth/logout', follow_redirects=True)

    with client.session_transaction() as sess:
        assert 'user_id' not in sess
    
    assert response.status_code == 200

#Aysin's code to test signup
def test_create_user_username(app, database):
    with app.app_context():
        # Create a user with random fake attributes
        user = create_user()

        # Retrieve the user from the database
        saved_user = UserModel.query.filter_by(username=user.username).first()

        # Assertions
        assert saved_user is not None  # Ensure user exists
        assert saved_user.id is not None  # Ensure ID is assigned
        assert saved_user.username == user.username
        assert saved_user.email == user.email
        assert saved_user.location == user.location

def test_create_user_email(app, database):
    with app.app_context():
        # Create a user with random fake attributes
        user = create_user()

        # Retrieve the user from the database
        saved_user = UserModel.query.filter_by(email=user.email).first()

        # Assertions
        assert saved_user is not None  # Ensure user exists
        assert saved_user.id is not None  # Ensure ID is assigned
        assert saved_user.username == user.username
        assert saved_user.email == user.email
        assert saved_user.location == user.location


    
def test_unique_user_details(app, database):
    with app.app_context():
        user = create_user("Frank", "frank@example.com", "London")
        #verify Frank has been created
        assert UserModel.query.filter_by(username = "Frank").first() is not None
        # Try creating a user with same email
        with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
            user = create_user("Aysin", "frank@example.com", "London")
        db.session.rollback()
        # Try creating a user with same username
        # with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
        #     user3 = UserModel(
        #         username = "Frank",
        #         password = "password123",
        #         email = "alister@example.com",
        #         phone_number = 111111111
        #     )
        #     db.session.add(user3)
        #     db.session.commit()
        # db.session.rollback()
        # # Try creating a user with same phone number
        # with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
        #     user4 = UserModel(
        #         username = "Alister",
        #         password = "password123",
        #         email = "louis@example.com",
        #         phone_number = 123456780
        #     )
        #     db.session.add(user4)
        #     db.session.commit()
        # db.session.rollback()
        assert UserModel.query.count() == 1, f"Expected 1 user, found {UserModel.query.count()}"
    