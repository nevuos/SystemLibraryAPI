import requests
import subprocess
import os
from api.utils.functions.important.check_internet_function import check_internet
from api.utils.logger.messager_logger import (
    INFO_UPDATE_AVAILABLE,
    INFO_UP_TO_DATE,
    INFO_UPDATE_SUCCESS,
    ERROR_NO_INTERNET,
    ERROR_REQUEST_FAILURE,
    ERROR_CODE_UPDATE_FAILURE,
)


REPO = "nevuos/SystemLibraryAPI"


def check_update(logger):
    if not check_internet():
        logger.info(ERROR_NO_INTERNET)
        return

    try:
        # Obtenha a versão mais recente do repositório do GitHub
        response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
        response.raise_for_status()  # Lança um erro se a solicitação falhar
        latest_version = response.json()['tag_name']
    except requests.exceptions.RequestException as e:
        logger.error(ERROR_REQUEST_FAILURE.format(error=e))
        return

    # Abra o arquivo de versão atual
    try:
        with open("version.txt", "r") as file:
            current_version = file.read().strip()
    except FileNotFoundError:
        current_version = None

    if current_version is None or latest_version > current_version:
        logger.info(INFO_UPDATE_AVAILABLE.format(version=latest_version))
        update_code(logger, latest_version)
    else:
        logger.info(INFO_UP_TO_DATE)


def update_code(logger, version):
    try:
        subprocess.check_call(["git", "pull", "origin", "master"])
        with open("version.txt", "w") as file:
            file.write(version)
    except subprocess.CalledProcessError as e:
        logger.error(ERROR_CODE_UPDATE_FAILURE.format(error=e))
        return

    logger.info(INFO_UPDATE_SUCCESS.format(version=version))
