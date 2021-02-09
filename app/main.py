from flask import (
    Blueprint,
    Flask,
)

from api.apikey.api import ns as ns_apikey
from api.auth.api import ns as ns_auth
from api.openapi.api import ns as ns_openapi
from api.restx import api


def create_app():
    app = Flask(__name__)
    app.config['BUNDLE_ERRORS'] = True

    # settinng
    app.config.from_pyfile("./configs/dev.py")

    # blueprints
    blueprint = Blueprint("api", __name__)
    api.init_app(blueprint)
    api.add_namespace(ns_openapi)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_apikey)

    app.register_blueprint(blueprint)

    return app


app = create_app()
