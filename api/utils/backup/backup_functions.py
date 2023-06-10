from supabase import create_client, Client
import os
import zipfile
import datetime
from api.utils.logger.messages_logger import (
    INFO_SOURCE_FOLDER_MISSING,
    INFO_BACKUP_FOLDER_CREATED,
    INFO_BACKUP_CREATED_LOCALLY,
    INFO_BACKUP_FOLDER_MISSING,
    INFO_BACKUP_UPLOAD_SUCCESS,
    ERROR_BACKUP_UPLOAD_FAILURE,
)

# Inicializa o cliente do Supabase
url: str = "https://paxkomehdsxnrmnyzlnc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBheGtvbWVoZHN4bnJtbnl6bG5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODYzOTk2ODgsImV4cCI6MjAwMTk3NTY4OH0.67iaymQtcPXdbiIPFI3cAR0O-RZXm0LAyCWMiHs_--w"
supabase: Client = create_client(url, key)


def backup_data_locally(logger):
    source_folder = "./instance"  # pasta de onde os dados serão copiados
    backup_folder = "./backup"  # pasta onde os backups locais serão armazenados

    # verifica se a pasta de origem existe
    if not os.path.isdir(source_folder):
        logger.info(INFO_SOURCE_FOLDER_MISSING.format(source_folder=source_folder))
        return

    # verifica se a pasta de backup existe, caso contrário, cria
    if not os.path.exists(backup_folder):
        try:
            os.makedirs(backup_folder)
            logger.info(INFO_BACKUP_FOLDER_CREATED.format(backup_folder=backup_folder))
        except OSError as e:
            logger.error(INFO_BACKUP_FOLDER_MISSING.format(backup_folder=backup_folder))
            return

    # cria um arquivo zip com os dados da pasta de origem
    zip_file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_backup.zip"
    zip_file_path = os.path.join(backup_folder, zip_file_name)
    zipf = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            zipf.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file),
                                    os.path.join(source_folder, '..')))
    zipf.close()

    logger.info(INFO_BACKUP_CREATED_LOCALLY.format(zip_file_name=zip_file_name))


def backup_data_to_supabase(logger):
    bucket_name = "Backup"  # o nome do seu bucket no Supabase
    subfolder_name = "teste"  # nome da subpasta que você quer criar no bucket
    backup_folder = "./backup"  # pasta onde os backups locais são armazenados

    # verifica se a pasta de backup local existe
    if not os.path.isdir(backup_folder):
        logger.info(INFO_BACKUP_FOLDER_MISSING.format(backup_folder=backup_folder))
        return

    # percorre todos os arquivos no diretório de backup e os carrega no Supabase
    for file_name in os.listdir(backup_folder):
        source = os.path.join(backup_folder, file_name)

        for attempt in range(3):  # tente fazer upload do arquivo 3 vezes
            try:
                with open(source, 'rb') as file:
                    response = supabase.storage.upload(bucket_name + "/" + subfolder_name + "/" + file_name, file)
                    if response.status_code == 200:  # se o status for 200, o upload foi bem-sucedido
                        logger.info(INFO_BACKUP_UPLOAD_SUCCESS.format(file_name=file_name))
                        break
            except Exception as e:
                logger.error(ERROR_BACKUP_UPLOAD_FAILURE.format(file_name=file_name, attempt=attempt + 1, error=str(e)))