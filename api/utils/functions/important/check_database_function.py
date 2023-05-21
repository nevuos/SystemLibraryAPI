import os
from api.utils.configurations.extensions import db
from api.utils.logger.messages_logger import INFO_DATABASE_NOT_FOUND, INFO_NEW_DATABASE_CREATED, INFO_DATABASE_FOUND
from flask import Flask


def check_database(app: Flask, logger):
    db_path = "instance/library.db"

    if not os.path.exists(db_path):
        logger.info(INFO_DATABASE_NOT_FOUND)

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        with app.app_context():
            db.create_all()

        logger.info(INFO_NEW_DATABASE_CREATED)
    else:
        logger.info(INFO_DATABASE_FOUND)
