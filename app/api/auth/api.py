import logging

from flask_restx import Resource, reqparse

from api.auth.db import AUTH_USERS
from api.auth.modules.decorator import jwt_authenticate
from api.auth.modules.encrypt import encrypt_jwt
from api import response as resp
from api.restx import api

logger = logging.getLogger(__name__)

ns = api.namespace("auth", description="Endpoints for user auth")

parser = reqparse.RequestParser()
parser.add_argument("username", required=True)
parser.add_argument("password", required=True)


@ns.route("/login")
class Login(Resource):
    def post(self):
        try:
            parsed = parser.parse_args()
        except Exception:
            return resp.invalid_param_error(
                "username, password must be specified",
            )

        # username and password check
        user = AUTH_USERS.get(parsed.username)
        if user is None or not user.check_password(parsed.password):
            return resp.bad_request("Invalid username or password")

        token = encrypt_jwt(user.username)
        return resp.ok({
            "access_token": token
        })


@ns.route("/me")
class Me(Resource):
    @jwt_authenticate()
    def get(self, **kwargs):
        user = kwargs["auth_user"]
        return resp.ok({
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
        })


@ns.route("/verify")
class Verify(Resource):
    @jwt_authenticate()
    def get(self, **kwargs):
        return resp.ok(msg="Token has been verified.")


@ns.route("/refresh")
class Refresh(Resource):
    @jwt_authenticate()
    def get(self, **kwargs):
        return resp.ok(
            {
                "access_token": encrypt_jwt(kwargs["jwt_username"])
            },
            msg="Token has been refreshed."
        )
