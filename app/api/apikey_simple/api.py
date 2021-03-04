import logging

from flask import request
from flask_restx import (
    Resource,
    reqparse,
)

from api import response as resp
from api.restx import api

logger = logging.getLogger(__name__)

ns = api.namespace("apikey-simple", description="Endpoints for simple api key service only for the example purpose")

parser = reqparse.RequestParser()
parser.add_argument("path", required=True)
parser.add_argument("raw_query", required=True)


# In-memory mock databases for users and whitelisted url paths
_users = {
    "token-1": "user-1",
}
_whitelists = ["/markets/all"]


@ns.route("/verify")
class Verify(Resource):
    def post(self, **kwargs):
        try:
            parsed = parser.parse_args()
        except Exception:
            return resp.error("Invalid request arguments")

        raw_token = request.headers.get("Authorization")
        if raw_token is None:
            return resp.unauthorized()

        if "Bearer " != raw_token[:7]:
            return resp.unauthorized("Token should have to start with 'Bearer '")

        token = raw_token[7:]

        # Check whether requested token is valid or not
        user_uuid = _users.get(token)
        if user_uuid is None:
            return resp.unauthorized("Unknown user")

        # Check whether requested url path is in th whitelist or not
        if parsed.path not in _whitelists:
            return resp.unauthorized("User has no permission on the path")

        return resp.ok(
            {"userUuid": user_uuid},
            msg="Verified",
        )
