from flask.testing import FlaskClient
from app.models import User
from sqlalchemy import select
from app.extensions import db
from flask_login import current_user

# Testing adapted from https://www.youtube.com/watch?v=OcD52lXq0e8&t=976s and https://flask.palletsprojects.com/en/3.0.x/testing/


def test_user_fixture(test_user: User):
    # Given the test user model
    # When a test User is created
    # Then check the user is created correctly
    assert test_user is not None
    assert test_user['first_name'] == 'Test'
    assert test_user['last_name'] == 'User'
    assert test_user['email_address'] == 'test@user.com'
    assert test_user['occupation'] == 'Tester'


def test_user_signup_existing_email(test_client: FlaskClient, test_user: dict):
    # Given the app is running and a user exists in the db
    # When a user signs up with an existing email address in the db
    # Then check the user is not created and the browser is redirected to the signup page and an error message is in the response
    response = test_client.post('/auth/signup', data=test_user)
    assert response.status_code == 400
    assert response.data == b'An account with this email address already exists'

    user = db.session.scalar(select(User).filter_by(email_address=test_user['email_address']))
    assert user is not None
    assert user.first_name == test_user['first_name']
    assert user.last_name == test_user['last_name']
    assert user.email_address == test_user['email_address']
    assert user.occupation == test_user['occupation']


def test_login_page(test_client: User):
    # Given the app is running
    # When the login page is requested
    # Then check the response is 200
    response = test_client.get('/auth/login')
    assert response.status_code == 200


def test_user_login(test_client: FlaskClient, test_user: dict):
    # Given the app is running and a user exists in the db
    # When a user logs in
    # Then check the user is logged in and the browser is redirected to the profile page
    response = test_client.post('/auth/login', data=test_user)
    assert response.status_code == 302
    assert response.headers['Location'] == '/profile'
    assert current_user.is_authenticated
    assert current_user.is_active


def test_login_page_when_logged_in(test_client: FlaskClient, test_user: dict):
    # Given a running app and a logged in user
    # When the login page is requested
    # Then check the user is redirected to the profile page
    response = test_client.post('/auth/login', data=test_user)
    assert response.status_code == 302
    assert response.headers['Location'] == '/profile'

    response = test_client.get('/auth/login')
    assert response.status_code == 302
    assert response.headers['Location'] == '/profile'


def test_user_profile_logged_in(test_client: FlaskClient):
    # Given a running app and the user is logged in
    # When a user requests their profile
    # Then check the response is 200
    response = test_client.get('/profile')
    assert response.status_code == 200


def test_user_logout(test_client: FlaskClient):
    # Given an app where a user is logged in
    # When a user logs out
    # Then check the user is logged out
    response = test_client.get('/auth/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    response = test_client.get('/profile')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_user_profile_logged_out(test_client: FlaskClient):
    # Given the user is logged out
    # When the profile page is requested
    # Then check the browser is redirected to the login page
    response = test_client.get('/profile')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_user_logout_when_not_logged_in(test_client: FlaskClient):
    # Given user is not logged in
    # When a logout rquest is made
    # Then check the user is redirected to the login page
    response = test_client.get('/auth/logout')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_user_delete_account_when_not_logged_in(test_client: FlaskClient):
    # Given the user is not logged in
    # When a delete account request is made
    # Then check the user is redirected to the login page
    response = test_client.delete('/auth/delete-user')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']
