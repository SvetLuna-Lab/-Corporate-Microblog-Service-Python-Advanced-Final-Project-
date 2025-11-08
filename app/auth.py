# app/auth.py

from typing import Callable, Any, TypeVar, cast

from flask import request

from . import db
from .models import User
from .api.errors import api_error

F = TypeVar("F", bound=Callable[..., Any])


def get_current_user() -> User:
    api_key = request.headers.get("api-key")
    if not api_key:
        api_error("auth_error", "Missing api-key header", status_code=401)

    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        api_error("auth_error", "User not found for given api-key", status_code=401)

    return user


def require_user(func: F) -> F:
    def wrapper(*args: Any, **kwargs: Any):
        user = get_current_user()
        return func(user, *args, **kwargs)

    return cast(F, wrapper)
