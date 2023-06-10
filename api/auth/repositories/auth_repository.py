from api.auth.models.user import User
from api.utils.configurations.extensions import db

class AuthenticationError(Exception):
    pass

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user
