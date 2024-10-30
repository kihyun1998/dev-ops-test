from __future__ import annotations

import requests
from pydantic import ValidationError

from .datamodel import User, UserDict


def fetch_user_data(url: str) -> list[UserDict]:
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch data: {response.status_code}")

    users_data: list[UserDict] = response.json()  # 불완전한 데이터를 받을 수 있음
    return users_data


def validate_users(users: list[UserDict]) -> list[User]:
    valid_users = dict()

    for user_data in users:
        try:
            user = User(**user_data)
            valid_users[user.id] = user
        except ValidationError as e:
            print(f"Invalid user data skipped: {e}")

    return list(valid_users.values())


def filter_active_users(users: list[User]) -> list[User]:
    return [user for user in users if user.is_active]
