from flask import make_response
import json
import datetime


def ok(data: dict = {}, msg="", status=200):  # pylint: disable=invalid-name
    assert isinstance(data, dict)

    data["timestamp"] = datetime.datetime.now().isoformat()
    data["message"] = msg

    return make_response(json.dumps(data), status)


def bad_request(msg="Bad request"):
    return error(msg=msg, status=400)


def unauthorized(msg="Unauthoized"):
    return error(msg=msg, status=401)


def invalid_param_error(msg="Invalid parameter error"):
    return error(msg=msg, status=422)


def error(msg="System error", status=500):
    return make_response(json.dumps({
        "message": msg,
        "timestamp": datetime.datetime.now().isoformat()
    }), status)
