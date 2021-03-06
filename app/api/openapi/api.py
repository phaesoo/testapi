import logging

from flask_restx import Resource

from api import response as resp
from api.restx import api

logger = logging.getLogger(__name__)

ns = api.namespace("markets", description="Endpoints for Market data")


@ns.route("/all")
class Markets(Resource):
    def get(self):
        return resp.ok(msg="Get markets")


@ns.route("/<market_id>")
class Market(Resource):
    def get(self, market_id):
        return resp.ok(msg="Get market {}".format(market_id))


@ns.route("/<market_id>/matches")
class Matches(Resource):
    def get(self, market_id):
        return resp.ok(msg="Get recent matches {}".format(market_id))
