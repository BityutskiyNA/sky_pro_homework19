from flask import Flask
from flask_restx import Api

from config import Config
from create_data import data_create
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.user import users_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.app_context().push()
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)
    data_create()

app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)