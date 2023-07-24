from werkzeug.security import check_password_hash, generate_password_hash
from api.utils.configurations.extensions import db


class TemporaryUser(db.Model):
    __tablename__ = 'temporary_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))  
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password  
        self.email = email

    def check_password(self, password):
        return self.password == password  

    def get_password(self):
        return self.password
