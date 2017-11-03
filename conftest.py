import pytest
from flask_security.confirmable import confirm_user

from cafebabel import app as myapp
from cafebabel.core.commands import _dropdb, _initdb
from cafebabel.users.models import User


def pytest_runtest_setup():
    _initdb()


def pytest_runtest_teardown():
    _dropdb()


@pytest.fixture
def app():
    myapp.config['WTF_CSRF_ENABLED'] = False
    return myapp


@pytest.fixture(scope='session')
def user():
    user = User.objects.create(email='testy@example.com', password='secret')
    with myapp.app_context():
        confirm_user(user)
    return user


@pytest.fixture(scope='session')
def admin():
    return User.objects.get(email='admin@example.com')
