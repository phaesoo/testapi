import logging

import jwt
from flask import request
from flask_restx import (
    Resource,
    reqparse,
)

from api import response as resp
from api.apikey.db import APIKEY_TABLE
from api.restx import api

logger = logging.getLogger(__name__)

ns = api.namespace("apikey", description="Endpoints for api key service")

parser = reqparse.RequestParser()
parser.add_argument("path", required=True)
parser.add_argument("raw_query", required=True)


# @ns.route("/issue")
# class Issue(Resource):
#     def post(self):
#         try:
#             parsed = parser.parse_args()
#         except Exception:
#             return resp.invalid_param_error(
#                 "username, password must be specified",
#             )

#         # username and password check
#         user = AUTH_USERS.get(parsed.username)
#         if user is None or not user.check_password(parsed.password):
#             return resp.bad_request("Invalid username or password")

#         token = encrypt_jwt(user.username)
#         return resp.ok({
#             "access_key": token
#         })


@ns.route("/verify")
class Verify(Resource):
    def _check_payload(self, payload: dict, query_exists: bool):
        for k in ["access_key", "nonce"]:
            if k not in payload:
                raise ValueError("Required field not exists in payload: {}".format(k))

        if query_exists:
            if "query_hash" not in payload:
                raise ValueError("Required field not exists in payload: query_hash")

    def post(self, **kwargs):
        try:
            parsed = parser.parse_args()
        except Exception:
            return resp.error("Invalid request arguments")

        print(parsed.path, parsed.raw_query)

        token = request.headers.get("Authorization")
        if token is None:
            return resp.unauthorized()

        if "Bearer " != token[:7]:
            print("Token should have to start with 'Bearer '")
            return resp.unauthorized()

        jwt_token = token[7:]
        try:
            payload = jwt.decode(jwt_token, options={"verify_signature": False})
        except Exception as e:
            print("Error while decoding token: {}".format(str(e)))
            return resp.unauthorized()

        try:
            self._check_payload(payload, False)  # FIXME
        except ValueError as e:
            print("Error while checking payload", e)
            return resp.unauthorized(str(e))

        access_key = payload["access_key"]

        # Get apikey object by access_key
        apikey = APIKEY_TABLE.get(access_key)
        if apikey is None:
            print("access_key not found: {}".format(access_key))
            return resp.unauthorized()

        # Validate with secret_key from db
        try:
            jwt.decode(jwt_token, apikey.secret_key, algorithms=["HS256"])
        except jwt.InvalidSignatureError:
            print("InvalidSignatureError: {} {}".format(jwt_token, apikey.secret_key))
            return resp.unauthorized()

        return resp.ok(
            {"userUuid": apikey.user_uuid},
            msg="Verified",
        )
