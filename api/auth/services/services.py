from api.auth.models.user import User
from api.auth.repositories.user_repository import get_user_by_username, save_user


def create_user(username: str, password: str) -> User:
    user = User(username=username)
    user.set_password(password)
    save_user(user)
    return user

def check_user_credentials(username: str, password: str) -> User:
    user = get_user_by_username(username)
    if user is not None and user.check_password(password):
        return user
    else:
        return None
