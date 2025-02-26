import pytest
from models.user import *
from flask import *
from extension import db
from app import create_app
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

def test_logout(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/auth/logout', follow_redirects=True)

    with client.session_transaction() as sess:
        assert 'user_id' not in sess
    
    assert response.status_code == 200
    