import os
import logging
from api.utils.configurations.extensions import db
from api.utils.logger.messages_logger import INFO_DATABASE_NOT_FOUND, INFO_NEW_DATABASE_CREATED, INFO_DATABASE_FOUND


def check_database():
    db_path = "instance/library.db"

    if not os.path.exists(db_path):
        logging.info(INFO_DATABASE_NOT_FOUND)

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        db.create_all()

        logging.info(INFO_NEW_DATABASE_CREATED)
    else:
        logging.info(INFO_DATABASE_FOUND)
