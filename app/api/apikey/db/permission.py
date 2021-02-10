from typing import Dict, List


class Permission:
    _id = 0

    def __init__(
        self,
        apikey_id: int,
        blacklist_paths: List[str],
    ) -> None:
        self.apikey_id = apikey_id
        self.blacklist_paths = blacklist_paths


# mock database table for permission
PERM_TABLE: Dict[int, Permission] = {}


def add_permission(
    apikey_id: int,
    blacklist_paths: List[str] = [],
):
    PERM_TABLE[apikey_id] = Permission(apikey_id, blacklist_paths)


# add mock data
add_permission(0)
add_permission(1, ["/markets/all"])
