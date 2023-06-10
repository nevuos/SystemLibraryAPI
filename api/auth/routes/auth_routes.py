from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api.auth.request_handlers import (
    register_request_handler,
    login_request_handler,
    protected_request_handler,
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    return register_request_handler(request.get_json())

@auth_bp.route("/login", methods=["POST"])
def login():
    return login_request_handler(request.get_json())

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return protected_request_handler()