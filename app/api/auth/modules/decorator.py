import time
from functools import wraps

from flask import request

from api.auth.db import AUTH_USERS
from api.auth.modules.encrypt import decrypt_jwt
from api.response import error
from define import status


def jwt_authenticate(is_admin=False):
    def _jwt_authenticate(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token is None:
                return error(
                    "Token is not given",
                    status=status.ERROR_UNAUTHORIZED,
                )
            try:
                decoded_token = decrypt_jwt(token)
            except Exception as e:
                print(e)
                return error(
                    "Invalid token given",
                    status=status.ERROR_UNAUTHORIZED,
                )

            username = decoded_token["username"]

            user = AUTH_USERS.get(username)
            if user is None:
                return error(
                    "Invalid username in token: {}".format(username),
                    status=status.ERROR_UNAUTHORIZED,
                )

            exp = decoded_token["exp"]
            if exp < time.time():
                return error(
                    "Access token has been expired",
                    status=status.ERROR_UNAUTHORIZED,
                )

            if is_admin and not user.is_admin:
                return error("Admin only", status=status.ERROR_FORBIDDEN)

            kwargs["jwt_username"] = user.username
            kwargs["jwt_exp"] = exp
            kwargs["jwt_iat"] = decoded_token["iat"]
            kwargs["auth_user"] = user

            return f(*args, **kwargs)
        return decorated_function
    return _jwt_authenticate
