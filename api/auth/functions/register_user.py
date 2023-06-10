from api.auth.repositories import get_user_by_username, create_user
from .hash_password import hash_password

def register_user(username, password):
    user = get_user_by_username(username)
    if user:
        raise Exception("Username already exists")

    password_hash = hash_password(password)
    user = create_user(username, password_hash)
    return user
