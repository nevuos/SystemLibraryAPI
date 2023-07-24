import os
from functools import wraps
from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError
import traceback
import sys

class InvalidRequestError(ValueError):
    pass

class AuthenticationError(ValueError):
    pass

class ResourceNotFoundError(FileNotFoundError):
    pass

class PermissionDeniedError(PermissionError):
    pass

class TimeoutError(TimeoutError):
    pass

class UnexpectedError(Exception):
    pass

class EmailAlreadyConfirmedError(ValueError):
    pass


error_mapping = {
    InvalidRequestError: (400, "Invalid request"),
    EmailAlreadyConfirmedError: (400, "Email already confirmed"),
    AuthenticationError: (401, "Authentication failed"),
    ResourceNotFoundError: (404, "Resource not found"),
    PermissionDeniedError: (403, "Permission denied"),
    TimeoutError: (408, "Request timeout"),
    UnexpectedError: (500, "An unexpected error occurred"),
    NoAuthorizationError: (401, "Missing Authorization Header"), 
}

def handle_errors(func):
    @wraps(func)
    def error_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type = type(e)
            status_code, error_message = error_mapping.get(
                error_type, (500, "An unexpected error occurred"))

            traceback_details = "".join(traceback.format_exception(*sys.exc_info()))

            if os.getenv("FLASK_ENV") == "PROD":
                error_response = {
                    'error_type': str(error_type.__name__),
                    'error_message': error_message,
                    'error_details': str(e),
                }
            else:
                error_response = {
                    'error_type': str(error_type.__name__),
                    'error_message': error_message,
                    'error_details': str(e),
                    'traceback': traceback_details,
                }
            return jsonify(error_response), status_code
    return error_wrapper
