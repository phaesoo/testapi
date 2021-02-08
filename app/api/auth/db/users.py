from typing import Dict

from api.auth.modules.encrypt import encrypt_sha


class User:
    _id = 0

    def __init__(
        self,
        username: str,
        password: str,
        is_admin: bool = False
    ) -> None:
        self.id = User._id
        self.username = username
        self.hashed_password = encrypt_sha(password)
        self.is_admin = is_admin
        User._id += 1

    def check_password(self, target_password) -> bool:
        return self.hashed_password == encrypt_sha(target_password)


# mock user database
AUTH_USERS: Dict[str, User] = {}


def add_user(
    username: str,
    password: str,
    is_admin: bool = False
):
    AUTH_USERS[username] = User(username, password, is_admin)


# add mock users
add_user("test", "testpw")
