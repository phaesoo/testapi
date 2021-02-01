from api.restx import api
from api.openapi.api import ns
from flask import (
    Blueprint,
    Flask,
)


def create_app():
    app = Flask(__name__)
    app.config['BUNDLE_ERRORS'] = True

    # settinng
    app.config.from_pyfile("./settings.py")

    # blueprints
    blueprint = Blueprint("api", __name__)
    api.init_app(blueprint)
    api.add_namespace(ns)

    app.register_blueprint(blueprint)

    return app


app = create_app()
