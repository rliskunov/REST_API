import pytest
import sys

from videoblog import app, Base, engine, session as db_session
from videoblog.models import User

sys.path.append('..')
pytest.yield_fixture(scope='function')


@pytest.fixture(scope='function')
def testapp():
    _app = app

    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield app

    Base.metadata.drop_all(bind=engine)
    _app.connection.close()


@pytest.fixture(scope='function')
def session(testapp):
    context = app.app_context()
    context.push()

    yield db_session

    db_session.close_all()
    context.pop()


@pytest.fixture(scope='function')
def user(session):
    user = User(
        name="Testuser",
        email="test@test.ru",
        password="password"
    )
    session.add(user)
    session.commit()
    return user
