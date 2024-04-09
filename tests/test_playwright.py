from flask import Flask
from app.models import User
import requests
from playwright.sync_api import Page, BrowserContext, Browser


def test_server_is_up_and_running(live_server_flask: Flask, flask_port: int):
    # Given the server is running
    # When the user sends a get request to the index page
    # Then the server should respond with a 200 status code
    url = f"http://127.0.0.1:{flask_port}"
    response = requests.get(url)
    assert response.status_code == 200


def test_user_signup_and_login_sequence(live_server_flask: Flask, flask_port: int, page: Page):
    # Given the user is on the home page
    # When the user clicks the sign up link and fills out the sign up form
    # Then they can log in and then delete their account

    page.goto(f"http://127.0.0.1:{flask_port}/")
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name="Sign Up").click()
    page.get_by_placeholder("First Name").click()
    page.get_by_placeholder("First Name").fill("Cookie")
    page.get_by_placeholder("Last Name").click()
    page.get_by_placeholder("Last Name").fill("Monster")
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("whostole@thecookie.jar")
    page.get_by_placeholder("Occupation").click()
    page.get_by_placeholder("Occupation").fill("Chef")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("WeHateCake")
    page.get_by_role("button", name="Sign Up").click()
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill("whostole@thecookie.jar")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("WeHateCake")
    page.get_by_label("Remember me?").check()
    page.get_by_role("button", name="Log In").click()
    page.get_by_role("button", name="DELETE ACCOUNT").click()


def test_create_and_save_map(live_server_flask: Flask, flask_port: int, page: Page, test_user: User, create_browser_context: BrowserContext):
    # Given the user is logged in
    # When the user creates a map and saves it
    # Then the map is saved and the user can view it
    page = create_browser_context.new_page()
    page.goto(f"http://127.0.0.1:{flask_port}/")
    page.get_by_role("link", name="Create Map").click()
    page.get_by_role("button", name="2021").click()
    page.get_by_role("button", name="Travel Method").click()
    page.get_by_role("button", name="Bicycle").click()
    page.get_by_label("Min Colour").click()
    page.get_by_label("Min Colour").fill("#bb1b1b")
    page.get_by_label("Max Colour").click()
    page.get_by_label("Max Colour").fill("#080e68")
    page.get_by_placeholder("Untitled Map").click()
    page.get_by_placeholder("Untitled Map").fill("My Map")
    page.get_by_role("button", name="Save Map").click()
    page.get_by_role("link", name="My Maps").click()
    page.get_by_role("link", name="My Map").nth(1).click()
    assert page.get_by_label("Interactive chart", exact=True).get_by_text("Travel Method - Bicycle -").is_visible


def test_access_profile_page_logged_in(browser: Browser, live_server_flask: Flask, flask_port: int):
    # Given the user is logged in
    # When the user navigates to the profile page
    # Then the profile page is displayed
    context = browser.new_context(storage_state="tests/state.json")
    page = context.new_page()
    page.goto(f"http://127.0.0.1:{flask_port}/")
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name="Profile").click()
    assert page.get_by_role("heading", name="Profile").is_visible


def test_user_logout_when_logged_in(browser: Browser, live_server_flask: Flask, flask_port: int):
    # Given the user is logged in
    # When the user logs out
    # Then the user is redirected to the login page
    context = browser.new_context(storage_state="tests/state.json")
    page = context.new_page()
    page.goto(f"http://127.0.0.1:{flask_port}/")
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name="Logout").click()
    assert page.get_by_role("heading", name="Dashboard").is_visible


def test_access_profile_page_logged_out(page: Page, live_server_flask: Flask, flask_port: int):
    # Given the user is logged out
    # When the user navigates to the profile page
    # Then the user is redirected to the login page
    page.goto(f"http://127.0.0.1:{flask_port}/profile")
    assert page.get_by_role("heading", name="Log In").is_visible
