# utils/update.py
import requests
import subprocess
import os
from api.utils.functions.important.check_internet_function import check_internet


REPO = "user/repo"  # substitua com o usuário e nome do repositório no GitHub


def check_update():
    if not check_internet():
        print('Sem conexão com a internet.')
        return

    # Obtenha a versão mais recente do repositório do GitHub
    response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
    response.raise_for_status()  # Lança um erro se a solicitação falhar
    latest_version = response.json()['tag_name']

    # Abra o arquivo de versão atual
    try:
        with open("version.txt", "r") as file:
            current_version = file.read().strip()
    except FileNotFoundError:
        current_version = None

    if current_version is None or latest_version > current_version:
        print(f"Nova versão {latest_version} disponível.")
        update_code(latest_version)
    else:
        print("Está na versão mais recente.")


def update_code(version):
    subprocess.check_call(["git", "pull", "origin", "master"]
                          )  # ou a branch que você deseja
    with open("version.txt", "w") as file:
        file.write(version)
    print(f"Versão atualizada para {version}.")
