from api.utils.configurations.extensions import db
from datetime import datetime


class Book(db.Model):  # type: ignore
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    bar_code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    barcode_download_url = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deactivated_at = db.Column(db.DateTime)

    loans = db.relationship('Loan', backref='book', lazy=True)
