import os
from flask import request
from flask_jwt_extended import create_access_token
from api.auth.repositories.user_repository import UserRepository
from api.auth.repositories.temporary_user_repository import TemporaryUserRepository
from api.utils.validators.generic.validate_required import validate_required_fields
from api.utils.handlers.error_handlers import EmailAlreadyConfirmedError, handle_errors, AuthenticationError
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from api.services.email_service import send_email

@handle_errors
@validate_required_fields(['username', 'password', 'email'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if UserRepository.get_user_by_username(username) is not None or TemporaryUserRepository.get_temporary_user_by_username(username) is not None:
        raise AuthenticationError("Username already exists or is waiting for email confirmation")

    TemporaryUserRepository.create_temporary_user(username, password, email)

    s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    token = s.dumps(email, salt='email-confirm')
    confirmation_url = 'http://localhost:8080/api/auth/confirm_email/' + token
    confirmation_email_template_id = os.getenv('CONFIRMATION_EMAIL_TEMPLATE_ID')

    send_email(email, 'Confirm Your Email', confirmation_url, confirmation_email_template_id)

    return {"msg": "A confirmation email has been sent to you by email"}, 201

@handle_errors
@validate_required_fields(['username', 'password'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    user = UserRepository.get_user_by_username(username)
    temp_user = TemporaryUserRepository.get_temporary_user_by_username(username)

    if user is None and temp_user is None:
        raise AuthenticationError("Bad username or password")
    elif user is None and temp_user is not None:
        raise AuthenticationError("Please confirm your email before login")

    if not user.check_password(password):
        raise AuthenticationError("Bad username or password")

    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}, 200

@handle_errors
def confirm_email(token):  
    if not token:
        raise AuthenticationError('Missing token')

    s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        raise AuthenticationError('The confirmation link is invalid or has expired.')
        
    temporary_user = TemporaryUserRepository.get_temporary_user_by_email(email)
    
    if not temporary_user:
        raise EmailAlreadyConfirmedError('Invalid token or user already confirmed')
    
    UserRepository.create_user(temporary_user.username, temporary_user.password, temporary_user.email, is_hashed=True)  
    TemporaryUserRepository.delete_temporary_user(temporary_user)

    return {"msg": "Email confirmed!"}, 200

@handle_errors
@validate_required_fields(['email'])
def resend_confirmation():
    data = request.get_json()
    email = data.get('email')

    temporary_user = TemporaryUserRepository.get_temporary_user_by_email(email)
    if not temporary_user:
        raise AuthenticationError('User not found or already confirmed')

    s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    token = s.dumps(email, salt='email-confirm')
    confirmation_url = 'http://localhost:8080/api/auth/confirm_email/' + token
    confirmation_email_template_id = os.getenv('CONFIRMATION_EMAIL_TEMPLATE_ID')

    send_email(email, 'Confirm Your Email', confirmation_url, confirmation_email_template_id)

    return {"msg": "A confirmation email has been resent to you by email"}, 200

@handle_errors
@validate_required_fields(['email'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    user = UserRepository.get_user_by_email(email)
    if not user:
        raise AuthenticationError('User not found')

    s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    token = s.dumps(email, salt='password-reset')
    password_reset_url = 'http://localhost:8080/api/auth/reset_password/' + token
    password_reset_email_template_id = os.getenv('RESET_PASSWORD_EMAIL_TEMPLATE_ID')

    send_email(email, 'Reset Your Password', password_reset_url, password_reset_email_template_id)

    return {"msg": "A password reset email has been sent to you by email"}, 200

@handle_errors
@validate_required_fields(['token', 'new_password'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    s = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        raise AuthenticationError('The reset link is invalid or has expired.')

    user = UserRepository.get_user_by_email(email)
    if not user:
        raise AuthenticationError('User not found')

    UserRepository.update_password(user, new_password)

    return {"msg": "Password successfully reset!"}, 200
