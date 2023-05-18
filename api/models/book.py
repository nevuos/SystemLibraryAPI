from api.utils.configurations.extensions import db
from datetime import datetime


class Book(db.Model):
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

    total_copies = db.Column(db.Integer, nullable=False, default=0)
    available_copies = db.Column(db.Integer, nullable=False, default=0)

    loans = db.relationship('Loan', backref='book', lazy=True)
