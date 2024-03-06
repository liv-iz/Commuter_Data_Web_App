from flask.testing import FlaskClient
from app.models import User, Map
from sqlalchemy import select
from app.extensions import db
import json
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


def test_user_signup(test_client: FlaskClient, test_user: dict):
    # Given a running app
    # When a user signs up
    # Then check the user is created and the browser is redirected to the login page
    response = test_client.post('/auth/signup', data=test_user)
    assert response.status_code == 302
    assert response.headers['Location'] == '/auth/login'

    user = db.session.scalar(select(User).filter_by(email_address=test_user['email_address']))
    assert user is not None
    assert user.first_name == test_user['first_name']
    assert user.last_name == test_user['last_name']
    assert user.email_address == test_user['email_address']
    assert user.occupation == test_user['occupation']


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
    assert response.headers['Location'] == '/app/profile'
    assert current_user.is_authenticated
    assert current_user.is_active


def test_login_page_when_logged_in(test_client: FlaskClient, test_user: dict):
    # Given a running app and a logged in user
    # When the login page is requested
    # Then check the user is redirected to the profile page
    response = test_client.post('/auth/login', data=test_user)
    assert response.status_code == 302
    assert response.headers['Location'] == '/app/profile'

    response = test_client.get('/auth/login')
    assert response.status_code == 302
    assert response.headers['Location'] == '/app/profile'


def test_user_profile_logged_in(test_client: FlaskClient):
    # Given a running app and the user is logged in
    # When a user requests their profile
    # Then check the response is 200
    response = test_client.get('/app/profile')
    assert response.status_code == 200


def test_post_map(test_client: FlaskClient, test_map: dict):
    # Given a running app and a logged in user
    # When a new map is posted
    response = test_client.post('/api/maps', json=json.dumps(test_map))

    # Then check the new map is returned
    json_data = response.get_json()
    assert json_data['name'] == test_map['name']
    assert json_data['data'] == test_map['data']
    assert json_data['id'] is not None

    # And check the new map exists in the database
    map_in_db = db.session.scalar(select(Map).filter_by(id=json_data['id']))
    assert map_in_db.name == test_map['name']
    assert map_in_db.data == test_map['data']


def test_get_map(test_client: FlaskClient, test_map: dict):
    # Given a logged in user
    # When a map is requested
    response = test_client.get(f'/api/maps/{test_map['id']}')

    # Then check the map is returned
    json_data = response.get_json()
    assert json_data['id'] == test_map['id']
    assert json_data['name'] == test_map['name']
    assert json_data['data'] == test_map['data']


def test_update_map(test_client: FlaskClient, test_map: dict, update_test_map: dict):
    # Given a logged in user
    # When a map is updated
    response = test_client.put(f'/api/maps/{test_map['id']}', json=json.dumps(update_test_map))

    # Then check the map is updated
    json_data = response.get_json()
    assert json_data['updated_map']['id'] == test_map['id']
    assert json_data['updated_map']['name'] == update_test_map['name']
    assert json_data['updated_map']['data'] == update_test_map['data']

    # And check the map is updated in the database
    map_in_db = db.session.scalar(select(Map).filter_by(id=test_map['id']))
    assert map_in_db.name == update_test_map['name']
    assert map_in_db.data == update_test_map['data']


def test_update_map_when_map_does_not_exist(test_client: FlaskClient, test_map: dict, update_test_map: dict):
    # Given a logged in user
    # When a map is updated that does not exist
    # Then it inserts the map into the database
    response = test_client.put('/api/maps/999', json=json.dumps(update_test_map))

    # Check the map has been added to db and the response is 201
    map_in_db = db.session.scalar(select(Map).filter_by(id=999))
    assert map_in_db.name == update_test_map['name']
    assert map_in_db.data == update_test_map['data']
    assert response.status_code == 201


def test_delete_map(test_client: FlaskClient, test_map: dict):
    # Given a logged in user
    # When a map is deleted
    response = test_client.delete(f'/api/maps/{test_map['id']}')

    # Then check the map is deleted
    assert response.status_code == 200
    assert response.data == b'Map Deleted Successfully!'

    # And check the map no longer exists in the database
    map_in_db = db.session.scalar(select(Map).filter_by(id=test_map['id']))
    assert map_in_db is None


def test_user_delete_account(test_client: FlaskClient, test_user: dict, test_map: dict):
    # Given a logged in user
    # When the user deletes their account
    response = test_client.delete('/auth/delete-user')

    # Then check the user is logged out and the browser is redirected to the login page
    assert response.status_code == 302
    assert response.headers['Location'] == '/auth/login'
    assert not current_user.is_authenticated
    assert not current_user.is_active

    # And check the user no longer exists in the database
    user_in_db = db.session.scalar(select(User).filter_by(email_address=test_user['email_address']))
    assert user_in_db is None

    # And check the map no longer exists in the database
    map_in_db = db.session.scalar(select(Map).filter_by(id=test_map['id']))
    assert map_in_db is None


def test_user_logout(test_client: FlaskClient):
    # Given an app where a user is logged in
    # When a user logs out
    # Then check the user is logged out
    response = test_client.get('/auth/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == '/auth/login'

    response = test_client.get('/app/profile')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_user_profile_logged_out(test_client: FlaskClient):
    # Given the user is logged out
    # When the profile page is requested
    # Then check the browser is redirected to the login page
    response = test_client.get('/app/profile')
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


def test_get_maps_when_not_logged_in(test_client: FlaskClient):
    # Given the user is not logged in
    # When the maps are requested
    # Then check the user is redirected to the login page
    response = test_client.get('/api/maps')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_post_map_when_not_logged_in(test_client: FlaskClient, test_map: dict):
    # Given the user is not logged in
    # When a map is posted
    # Then check the user is redirected to the login page
    response = test_client.post('/api/maps', json=json.dumps(test_map))
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_delete_map_when_not_logged_in(test_client: FlaskClient, test_map: dict):
    # Given the user is not logged in
    # When a map is deleted
    # Then check the user is redirected to the login page
    response = test_client.delete(f'/api/maps/{test_map['id']}')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_update_map_when_not_logged_in(test_client: FlaskClient, test_map: dict, update_test_map: dict):
    # Given the user is not logged in
    # When a map is updated
    # Then check the user is redirected to the login page
    response = test_client.put(f'/api/maps/{test_map['id']}', json=json.dumps(update_test_map))
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']
