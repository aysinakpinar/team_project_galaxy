from playwright.sync_api import Page, expect
from models.user import UserModel
import pytest


# # Test dashboard leaderboard displays data using Playwright -- | Michal |
# def test_dashboard_leaderboard_displays_correct_data(page, create_user, create_friendship, create_user_point): 
#     #create users in the database
#     user_1 = create_user(username='test_user', password="Test12345!", email="test@email.com", location="test_location")
#     user_2 = create_user(username='test_user_2', password="Test12345!", email="test2@email.com", location="test_location_2")
#     user_3 = create_user(username='test_user_3', password="Test12345!", email="test3@email.com", location="test_location_3")
#     #create friendships in the database
#     user_1_to_user_2_friendship = create_friendship(user_id=1, friend_id=2)
#     user_1_to_user_3_friendship = create_friendship(user_id=1, friend_id=3)
#     #create points in the database
#     user_1_points = create_user_point(weekly_points=10, monthly_points=20, yearly_points=100, user_id=1)
#     user_2_points = create_user_point(weekly_points=15, monthly_points=30, yearly_points=80, user_id=2)
#     user_3_points = create_user_point(weekly_points=25, monthly_points=25, yearly_points=300, user_id=3)

#     page.goto("http://127.0.0.1:5000/auth/login")

#     # fill up the login form on the page
#     email_input = page.get_by_label("Email")
#     email_input.fill("test@email.com")
#     password_input = page.get_by_label("Password")
#     password_input.fill("Test12345!")
#     submit_button = page.get_by_text("Submit")
#     submit_button.click()
#     # successful login will redirect to the dashboard page
#     assert page.url == "http://127.0.0.1:5000/dashboard"

#     # weekly points assertion
#     user_2_in_friends = page.get_by_text("test_user_2")
#     assert user_2_in_friends.is_visible()
#     user_3_in_friends = page.get_by_text("test_user_3")
#     assert user_3_in_friends.is_visible()





