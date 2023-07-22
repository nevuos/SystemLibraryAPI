
from flask import Blueprint
from api.auth.request_handlers.auth_handlers import register, login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def handle_register_request():
    return register()

@auth_bp.route('/login', methods=['POST'])
def handle_login_request():
    return login()
