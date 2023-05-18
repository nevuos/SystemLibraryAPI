from datetime import datetime
from api.utils.configurations.extensions import db


class Student(db.Model):  # type: ignore
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    registration_number = db.Column(
        db.String(100), index=True, unique=True, nullable=False)
    class_name = db.Column(db.String(100), nullable=True)
    grade = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deactivated_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), default='active')
    loans = db.relationship('Loan', backref='student', lazy=True)
