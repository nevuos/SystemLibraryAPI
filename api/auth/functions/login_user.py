from api.auth.repositories import get_user_by_username
from .verify_password import verify_password

def login_user(username, password):
    user = get_user_by_username(username)
    if not user:
        raise Exception("Invalid username or password")

    password_match = verify_password(user.password_hash, password)
    if not password_match:
        raise Exception("Invalid username or password")

    return user
