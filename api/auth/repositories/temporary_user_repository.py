from api.auth.models.temporary_user import TemporaryUser
from api.utils.configurations.extensions import db


class TemporaryUserRepository:
    @staticmethod
    def get_temporary_user_by_username(username):
        return TemporaryUser.query.filter_by(username=username).first()

    @staticmethod
    def get_temporary_user_by_email(email):
        return TemporaryUser.query.filter_by(email=email).first()

    @staticmethod
    def create_temporary_user(username, password, email):
        user = TemporaryUser(username, password, email)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete_temporary_user(temporary_user):
        db.session.delete(temporary_user)
        db.session.commit()