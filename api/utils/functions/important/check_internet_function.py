import socket

from api.utils.logger.messages_logger import ERROR_NO_INTERNET, INFO_INTERNET_SUCCESS

def check_internet(logger):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        logger.info(INFO_INTERNET_SUCCESS)
        return True
    except OSError:
        logger.error(ERROR_NO_INTERNET)
        return False
