from playwright.sync_api import Page, expect
from models.user import UserModel
import pytest

# # create_user fixture -- | Michal |
@pytest.fixture
def create_user(database):
    """Fixture to add a user to the database."""
    # Create a user instance
    test_user = UserModel(
        id=None,
        username='test_user',
        password="Test12345!", 
        email="test@email.com",
        location="test_location"
    )
    database.session.add(test_user)
    database.session.commit()
    yield test_user



# Test login function with correct data using Playwright -- | Michal |
def test_correct_login_details_redirects_to_dashboard_in_browser(database, create_user, page):   
            page.goto("http://127.0.0.1:5000/auth/login")

            # fill up the login form on the page
            email_input = page.get_by_label("Email")
            email_input.fill("test@email.com")
            password_input = page.get_by_label("Password")
            password_input.fill("Test12345!")
            submit_button = page.get_by_text("Submit")
            submit_button.click()

            assert page.url == "http://127.0.0.1:5000/dashboard"

# Test login function with incorrect data using Playwright -- | Michal |
def test_incorrect_login_details_shows_error_in_browser(create_user, page):   
        # create test user in the database
        create_test_user = create_user
        # navigate to a website
        page.goto("http://127.0.0.1:5000/auth/login")

        # fill up the login form on the page
        email_input = page.get_by_label("Email")
        email_input.fill("wrong@email.com")
        # Check if error tag is displayed
        email_error_tag = page.get_by_text("Wrong email address")
        assert email_error_tag.is_visible

        password_input = page.get_by_label("Password")
        password_input.fill("WrongPassword")
        # Check if error tag is displayed
        password_error_tag = page.get_by_text("Wrong password")
        assert password_error_tag.is_visible