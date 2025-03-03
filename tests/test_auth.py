from playwright.sync_api import Page, expect, sync_playwright
from models.user import UserModel
import pytest


# Test login function with correct data using Playwright -- | Michal |
# def test_create_user(create_user):   
#         #create user in the database
#         user = create_user(username='test_user', password="Test12345!", email="test@email.com", location="test_location")
#         playwright = sync_playwright().start()
#         browser = playwright.chromium.launch(headless=False, slow_mo=500)
#         page = browser.new_page()
        
#         saved_user = UserModel.query.filter_by(email=user.email).first()

#         page.goto("http://127.0.0.1:5000/auth/login")

#         # fill up the login form on the page
#         email_input = page.get_by_label("Email")
#         email_input.fill("test@email.com")
#         password_input = page.get_by_label("Password")
#         password_input.fill("Test12345!")
#         submit_button = page.get_by_text("Submit")
#         submit_button.click()

#         assert page.url == "http://127.0.0.1:5000/dashboard"
        
# Test login function with incorrect data using Playwright -- | Michal |
# def test_incorrect_login_details_shows_error_in_browser(create_user, page):   
#         # create test user in the database
#         create_user(username='test_user', password="Test12345!", email="test@email.com", location="test_location")
#         # navigate to a website
#         page.goto("http://127.0.0.1:5000/auth/login")

#         # fill up the login form on the page with wrong email address
#         email_input = page.get_by_label("Email")
#         email_input.fill("wrong@email.com")
#         password_input = page.get_by_label("Password")
#         password_input.fill("WrongPassword")
#         submit_button = page.get_by_text("Submit")
#         submit_button.click()
#         # check if error tag is displayed
#         email_error_tag = page.get_by_text("Wrong email address")
#         assert email_error_tag.is_visible()

#         # correct email address, wrong password
#         email_input.fill("test@email.com")
#         password_input.fill("WrongPassword")
#         submit_button.click()
#         # check if error tag is displayed
#         password_error_tag = page.get_by_text("Wrong password")
#         assert password_error_tag.is_visible()