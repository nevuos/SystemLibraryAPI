from functools import wraps
from flask import jsonify
from functools import wraps
from flask import jsonify
from werkzeug.exceptions import HTTPException
from typing import Dict, Tuple
import traceback
import sys



error_mapping: Dict[type, Tuple[int, str]] = {
    ValueError: (400, "Invalid request"),
    KeyError: (400, "Invalid request"),
    IndexError: (400, "Invalid request"),
    FileNotFoundError: (404, "File not found"),
    PermissionError: (403, "Permission denied"),
    TimeoutError: (408, "Request timeout"),
    Exception: (500, "Internal server error")
}


def handle_errors(func):
    @wraps(func)
    def error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type = type(e)
            if error_type in error_mapping:
                status_code, error_message = error_mapping[error_type]
                error_details = str(e)
            elif issubclass(error_type, HTTPException):
                status_code, error_message = e.code, e.description
                error_details = str(e)
            else:
                status_code, error_message = 500, "An unexpected error occurred during the operation."
                error_details = str(e)

            traceback_details = "".join(traceback.format_exception(*sys.exc_info()))
            error_response = {
                'error_type': str(error_type.__name__),
                'error_message': error_message,
                'error_details': error_details,
                'traceback': traceback_details,
            }
            return jsonify(error_response), status_code
    return error_wrapper
