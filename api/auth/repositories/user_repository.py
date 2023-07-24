from api.utils.configurations.extensions import db
from api.auth.models.user import User
from werkzeug.security import generate_password_hash

class UserRepository:
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username, password, email, is_hashed=False):
        password_hash = password if is_hashed else generate_password_hash(password)
        user = User(username, password_hash, email)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def update_password(user, new_password):
        user.password_hash = generate_password_hash(new_password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()