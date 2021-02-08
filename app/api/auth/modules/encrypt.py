import time
from hashlib import sha256

import jwt

from configs import get_config

# iat: issued at
# exp: expiration time


def __validate_jwt(data):
    for key in ["username", "iat", "exp"]:
        if key not in data:
            raise KeyError


def encrypt_jwt(username):
    iat = time.time()
    exp = iat + get_config("JWT_EXP_PERIOD")
    return jwt.encode({
        "username": username,
        "iat": iat,
        "exp": exp
    }, get_config("JWT_SECRET_KEY"), algorithm=get_config("JWT_ALGO"))


def decrypt_jwt(token):
    data = jwt.decode(token, get_config("JWT_SECRET_KEY"),
                      algorithms=[get_config("JWT_ALGO")])
    __validate_jwt(data)
    return data


def encrypt_sha(hash_string):
    return sha256(hash_string.encode()).hexdigest()
