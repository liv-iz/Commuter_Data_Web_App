from app import create_app
import pytest
from app.extensions import db
import socket
import subprocess
import time
from app.models import User
from playwright.sync_api import Browser


@pytest.fixture(scope='module')
def test_user():
    return {
        'first_name': 'Test',
        'last_name': 'User',
        'email_address': 'test@user.com',
        'occupation': 'Tester',
        'password': 'password'
    }


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as client:
        yield client

    # Drop test database tables
    with flask_app.app_context():
        db.drop_all()


@pytest.fixture(scope="session")
def flask_port():
    """Gets a free port from the operating system."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="session")
def live_server_flask(flask_port):
    #  Runs the Flask app as a live server for Playwright tests
    #  Renamed to live_server_flask to avoid issues with pytest-flask live_server
    #  Assumes venv is active!!!

    command = f"""poetry run python -m flask run --debug --port={flask_port}"""
    try:
        server = subprocess.Popen(command, shell=True)
        # Allow time for the app to start
        time.sleep(3)
        yield server
        server.terminate()
    except subprocess.CalledProcessError as e:
        print(f"Error starting Flask app: {e}")


@pytest.fixture()
def create_browser_context(browser: Browser, test_user: User, flask_port):
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Navigate to the login page and fill out the form
    page.goto(f"http://127.0.0.1:{flask_port}/")
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name="Sign Up").click()
    page.get_by_placeholder("First Name").click()
    page.get_by_placeholder("First Name").fill(test_user["first_name"])
    page.get_by_placeholder("Last Name").click()
    page.get_by_placeholder("Last Name").fill(test_user["last_name"])
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill(test_user["email_address"])
    page.get_by_placeholder("Occupation").click()
    page.get_by_placeholder("Occupation").fill(test_user["occupation"])
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(test_user["password"])
    page.get_by_role("button", name="Sign Up").click()
    page.get_by_placeholder("Email Address").click()
    page.get_by_placeholder("Email Address").fill(test_user["email_address"])
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(test_user["password"])
    page.get_by_label("Remember me?").check()
    page.get_by_role("button", name="Log In").click()
    time.sleep(2)
    context.storage_state(path="tests/state.json")
    yield context
    context.close()
