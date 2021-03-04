import hashlib
import logging

import jwt
from flask import request
from flask_restx import (
    Resource,
    reqparse,
)

from api import response as resp
from api.apikey.db import APIKEY_TABLE
from api.apikey.db.permission import PERM_TABLE
from api.restx import api

logger = logging.getLogger(__name__)

ns = api.namespace("apikey", description="Endpoints for api key service")

parser = reqparse.RequestParser()
parser.add_argument("path", required=True)
parser.add_argument("raw_query", required=True)


def sha512(s: str) -> str:
    return hashlib.sha512(s.encode()).hexdigest()


@ns.route("/verify")
class Verify(Resource):
    def _check_payload(self, payload: dict, query_exists: bool):
        for k in ["access_key", "nonce"]:
            if k not in payload:
                raise ValueError("Required field not exists in payload: {}".format(k))

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

        query_hash = payload.get("query_hash")
        if query_hash:
            hashed = sha512(parsed.raw_query)
            print(query_hash, hashed)

        access_key = payload["access_key"]

        # Get apikey object by access_key
        apikey = APIKEY_TABLE.get(access_key)
        if apikey is None:
            print("access_key not found: {}".format(access_key))
            return resp.unauthorized()

        permission = PERM_TABLE.get(apikey.id)
        if permission:
            if parsed.path in permission.blacklist_paths:
                print("Try to use blacklist path: {}, {}".format(apikey.id, parsed.path))
                return resp.bad_request("APIKey({}) has no permission for path: {}".format(apikey.id, parsed.path))
        else:
            print("[ERROR] There is no permission for APIKey: {}".format(apikey.id))

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
