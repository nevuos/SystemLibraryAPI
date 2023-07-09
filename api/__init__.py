from flask import Flask
from api.routes.book.book_routes import book_bp
from api.routes.download.download_routes import download_bp
from api.routes.index.index_routes import index_bp
from api.routes.loan.loan_routes import loan_bp
from api.routes.student.student_routes import student_bp
from api.utils.backup.backup import do_backup
from api.utils.configurations.config import Config
from api.utils.configurations.extensions import db, migrate
from api.utils.cache.cache import init_cache
from api.utils.functions.important.check_internet_function import check_internet
from api.utils.logger.logger import setup_logger
#from api.utils.update.check_update_function import check_update
from api.utils.functions.important.check_database_function import check_database
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def create_app():
    """
    Cria e configura o aplicativo Flask.
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)


    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    with flask_app.app_context():
        db.create_all()
        logger = setup_logger(__name__)
    
        check_internet(logger)
        #check_update(logger)
        check_database(flask_app, logger)
        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: do_backup(logger), CronTrigger(hour=12))
        scheduler.start()

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
