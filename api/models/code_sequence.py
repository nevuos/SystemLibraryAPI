from api.utils.configurations.extensions import db


class CodeSequence(db.Model):  # type: ignore
    __tablename__ = 'code_sequence'
    id = db.Column(db.Integer, primary_key=True)
