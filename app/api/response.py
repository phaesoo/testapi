from flask import make_response
import json
import datetime


def ok(data: dict = {}, msg="", status=200):
    assert isinstance(data, dict)

    data["timestamp"] = datetime.datetime.now().isoformat()
    data["message"] = msg

    return make_response(json.dumps(data), status)


def error(msg="System error", status=500):
    return make_response(json.dumps({
        "message": msg,
        "timestamp": datetime.datetime.now().isoformat()
    }), status)
