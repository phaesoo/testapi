from typing import Dict
from uuid import UUID, uuid4


class APIKey:
    _id = 0

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        user_uuid: UUID,
    ) -> None:
        self.id = APIKey._id
        self.access_key = access_key
        self.secret_key = secret_key
        self.user_uuid = str(user_uuid)
        APIKey._id += 1


# mock database table for apikey
APIKEY_TABLE: Dict[str, APIKey] = {}


def add_apikey(
    access_key: str,
    secret_key: str,
    user_uuid: UUID,
):
    APIKEY_TABLE[access_key] = APIKey(access_key, secret_key, user_uuid)


# add mock apikey
add_apikey("123", "456", uuid4())
add_apikey("789", "012", uuid4())
