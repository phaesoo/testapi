# flake8: noqa
import os
import json
import tempfile
import pytest

import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../../app")

from main import create_app 


@pytest.fixture(scope="session")
def client():
    app = create_app()

    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    print(app.url_map)

    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def parse_body(resp):
    return json.loads(resp.data.decode("utf-8"))

# register custom function
sys.modules['pytest'].parse_body = parse_body