from api.utils.configurations.extensions import db
from datetime import datetime, timedelta


class Loan(Model):  # type: ignore
    __tablename__ = 'loan'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id'), nullable=False, index=True)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow() + timedelta(days=7))
    returned = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    deactivated_at = db.Column(db.DateTime, nullable=True)
