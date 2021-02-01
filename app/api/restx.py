import logging
from flask_restx import Api
from api import response as resp


logger = logging.getLogger(__name__)
api = Api(version="1.0.0", title="Flask-JWT-Auth Example")


@api.errorhandler
def default_error_handler(e):
    message = "Unhandled exception occurred: {}".format(e)
    logger.exception(message)
    return resp.error(message)
