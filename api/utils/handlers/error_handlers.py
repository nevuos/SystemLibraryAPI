from functools import wraps
from flask import jsonify
from typing import Any, Callable, Dict, Tuple

error_mapping: Dict[type, int] = {
    ValueError: 400,
    KeyError: 400,
    IndexError: 400,
    FileNotFoundError: 404,
    PermissionError: 403,
    TimeoutError: 408,
    Exception: 500
}


def handle_errors(func: Callable[..., Tuple[Any, int]]) -> Callable[..., Tuple[Any, int]]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Tuple[Any, int]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type: type = type(e)
            error_message: str = "Ocorreu um erro durante a execução da operação."
            return jsonify({'error': error_message, 'details': str(e)}), error_mapping.get(error_type, 500)
    return wrapper
