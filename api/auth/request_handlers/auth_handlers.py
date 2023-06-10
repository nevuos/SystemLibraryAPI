from flask import jsonify
from api.auth.functions import register_user, verify_password
from api.auth.repositories.auth_repository import get_user_by_username
from flask_jwt_extended import create_access_token
from api.utils.handlers import handle_errors


@handle_errors
def register_request_handler(request_data):
    username = request_data.get("username")
    password = request_data.get("password")

    if not username or not password:
        return jsonify({"error": "Nome de usuário ou senha inválidos"}), 400

    register_user(username, password)
    return jsonify({"message": "Usuário registrado com sucesso"}), 201


@handle_errors
def login_request_handler(request_data):
    username = request_data.get("username")
    password = request_data.get("password")

    if not username or not password:
        return jsonify({"error": "Nome de usuário ou senha inválidos"}), 400

    user = get_user_by_username(username)
    if not user or not verify_password(user.password_hash, password):
        return jsonify({"error": "Nome de usuário ou senha inválidos"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200


@handle_errors
def protected_request_handler(request_data):
    return jsonify({"message": "Rota protegida"}), 200
