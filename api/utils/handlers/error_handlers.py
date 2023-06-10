from functools import wraps
from flask import jsonify
from typing import Any, Callable, Dict, Tuple
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from api.auth.repositories.auth_repository import AuthenticationError


error_mapping: Dict[type, Tuple[int, str]] = {
    ValueError: (400, "Invalid request"),
    KeyError: (400, "Invalid request"),
    IndexError: (400, "Invalid request"),
    FileNotFoundError: (404, "File not found"),
    PermissionError: (403, "Permission denied"),
    TimeoutError: (408, "Request timeout"),
    AuthenticationError: (401, "Authentication failed"),
    ExpiredSignatureError: (401, "Token expired"),
    InvalidTokenError: (401, "Invalid token"),
    Exception: (500, "Internal server error")
}


def handle_errors(func: Callable[..., Tuple[Any, int]]) -> Callable[..., Tuple[Any, int]]:
    @wraps(func)
    def error_wrapper(*args: Any, **kwargs: Any) -> Tuple[Any, int]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type: type = type(e)
            error_message: str = "An error occurred during the operation."

            if error_type in error_mapping:
                status_code, error_message = error_mapping[error_type]
            else:
                status_code, _ = error_mapping[Exception]

            return jsonify({'error': error_message, 'details': str(e)}), status_code

    return error_wrapper
