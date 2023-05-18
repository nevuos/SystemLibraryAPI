"""
Este é o módulo de inicialização do Flask para a aplicação.
"""

from flask import Flask
from api.routes.book.book_routes import book_bp
from api.routes.download.download_routes import download_bp
from api.routes.index.index_routes import index_bp
from api.routes.loan.loan_routes import loan_bp
from api.routes.student.student_routes import student_bp
from api.utils.configurations.config import Config
from api.utils.configurations.extensions import db, migrate
from api.utils.cache.cache import init_cache


def create_app():
    """
    Cria e configura o aplicativo Flask.
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    flask_app.register_blueprint(student_bp, url_prefix='/api')
    flask_app.register_blueprint(book_bp, url_prefix='/api')
    flask_app.register_blueprint(loan_bp, url_prefix='/api')
    flask_app.register_blueprint(download_bp, url_prefix='/api')
    flask_app.register_blueprint(index_bp, url_prefix='/api')

    init_cache(flask_app)

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run()
