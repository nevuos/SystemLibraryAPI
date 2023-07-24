from flask import Blueprint
from api.utils.configurations.extensions import limiter
from api.auth.request_handlers.auth_handlers import confirm_email, register, login, request_password_reset, resend_confirmation, reset_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_register_request():
    return register()

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_login_request():
    return login()

@auth_bp.route('/confirm_email/<token>', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def confirm_email_route(token):
    return confirm_email(token)

@auth_bp.route('/resend_confirmation', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def resend_confirmation_route():
    return resend_confirmation()

@auth_bp.route('/reset_password_request', methods=['POST'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_reset_password_request():
    return request_password_reset()

@auth_bp.route('/reset_password/<token>', methods=['GET'])
@limiter.limit("1000/day;100/hour;30/minute")
def handle_reset_password(token):
    return reset_password(token)