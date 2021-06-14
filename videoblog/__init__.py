import logging
from logging import FileHandler, Formatter, Logger
from typing import Union, Any

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask.testing import FlaskClient
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeMeta

from videoblog.config import Config
from videoblog.schemas import VideoSchema, UserSchema, AuthSchema

app: Flask = Flask(__name__)
app.config.from_object(Config)

client: FlaskClient = app.test_client()

engine: Union[MockConnection, Any] = create_engine('sqlite:///db.sqlite')
session: scoped_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base: Union[DeclarativeMeta, Any] = declarative_base()
Base.query = session.query_property()

jwt = JWTManager()

docs = FlaskApiSpec()
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})

from videoblog.models import Video, User

Base.metadata.create_all(bind=engine)


def setup_logger() -> Logger:
    logger: Logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter: Formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
    )
    file_handler: FileHandler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from videoblog.main.views import videos
from videoblog.users.views import users

app.register_blueprint(users)
app.register_blueprint(videos)

docs.init_app(app)
jwt.init_app(app)
