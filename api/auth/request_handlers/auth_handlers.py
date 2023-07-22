from flask import request
from flask_jwt_extended import create_access_token
from api.auth.models.user import User
from api.auth.repositories.user_repository import UserRepository
from api.utils.validators.generic.validate_required import validate_required_fields
from api.utils.handlers.error_handlers import handle_errors, AuthenticationError


@validate_required_fields(['username', 'password'])
@handle_errors
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    if UserRepository.get_user_by_username(username) is not None:
        raise AuthenticationError("Username already exists")

    UserRepository.create_user(username, password)

    return {"msg": "User created"}, 201

@validate_required_fields(['username', 'password'])
@handle_errors
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    user = UserRepository.get_user_by_username(username)
    if user is None or not user.check_password(password):
        raise AuthenticationError("Bad username or password")

    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}, 200
