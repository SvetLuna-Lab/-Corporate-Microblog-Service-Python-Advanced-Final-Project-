# app/api/errors.py

from typing import Any
from flask import Blueprint, jsonify

errors_bp = Blueprint("errors", __name__)


def api_error(error_type: str, error_message: str, status_code: int = 400) -> Any:
    response = jsonify(
        {
            "result": False,
            "error_type": error_type,
            "error_message": error_message,
        }
    )
    response.status_code = status_code
    # Немедленно прерываем выполнение через исключение
    raise _APIError(response)


class _APIError(Exception):
    def __init__(self, response):
        self.response = response


@errors_bp.app_errorhandler(_APIError)
def handle_api_error(exc: _APIError):
    return exc.response
