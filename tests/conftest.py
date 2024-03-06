from app import create_app
import pytest
from app.extensions import db


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


@pytest.fixture(scope='module')
def test_map():
    return {
        'id': 1,
        'name': 'Test map',
        'data': 'This is a test map',
    }


@pytest.fixture(scope='module')
def update_test_map():
    return {
        'name': 'UPDATED test map name',
        'data': 'UPDATED test map data',
    }
