import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask
from api.routes.book.book_routes import book_bp
from api.routes.download.download_routes import download_bp
from api.routes.index.index_routes import index_bp
from api.routes.loan.loan_routes import loan_bp
from api.routes.student.student_routes import student_bp
from api.utils.backup.backup import do_backup
from api.utils.cache.cache import init_cache
from api.utils.configurations.config import Config
from api.utils.configurations.extensions import db, migrate
from api.utils.functions.important.check_database_function import check_database
from api.utils.functions.important.check_internet_function import check_internet
from api.utils.logger.logger import setup_logger
from api.utils.update.update_application import update_application
from api.auth.routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
from api.utils.configurations.extensions import limiter


def create_app():
    """
    Cria e configura o aplicativo Flask.
    """
    load_dotenv()
    
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    
    flask_app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    JWTManager(flask_app)

    limiter.init_app(flask_app)
    
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    with flask_app.app_context():
        db.create_all()
        logger = setup_logger(__name__)
        update_application(logger)
        check_internet(logger)
        check_database(flask_app, logger)
        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: do_backup(logger), CronTrigger(hour=12))
        scheduler.start()

    flask_app.register_blueprint(student_bp, url_prefix='/api')
    flask_app.register_blueprint(book_bp, url_prefix='/api')
    flask_app.register_blueprint(loan_bp, url_prefix='/api')
    flask_app.register_blueprint(download_bp, url_prefix='/api')
    flask_app.register_blueprint(index_bp, url_prefix='/api')
    flask_app.register_blueprint(auth_bp, url_prefix='/api/auth')

    init_cache(flask_app)

    return flask_app

if __name__ == '__main__':
    app = create_app()
    app.run()
