# # from playwright.sync_api import Page, expect
# from playwright.async_api import async_playwright
# from models.user import UserModel
# import pytest

# # Test login function with correct data using Playwright -- | Michal |
# async def test_correct_login_details_redirects_to_dashboard_in_browser(
#     database, create_some_users, create_some_friendships, create_some_user_points
# ):
#     async with async_playwright() as p:  
#         browser = p.chromium.launch(headless=False, slow_mo=500)  # Opens browser, slows actions
#         page = browser.new_page()
        
#         page.goto("http://127.0.0.1:5000/auth/login")

#         # fill up the login form on the page
#         email_input = page.get_by_label("Email")
#         email_input.fill("test@email.com")
#         password_input = page.get_by_label("Password")
#         password_input.fill("Test12345!")
#         submit_button = page.get_by_text("Submit")
#         submit_button.click()

#         assert page.url == "http://127.0.0.1:5000/dashboard"
#         browser.close()




