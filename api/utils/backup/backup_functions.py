import os
import zipfile
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from api.utils.logger.messages_logger import (
    INFO_SOURCE_FOLDER_MISSING,
    INFO_BACKUP_FOLDER_CREATED,
    INFO_BACKUP_CREATED_LOCALLY,
    INFO_BACKUP_FOLDER_MISSING,
    INFO_BACKUP_UPLOAD_SUCCESS,
    ERROR_BACKUP_UPLOAD_FAILURE,
)


def backup_data_locally(logger):
    source_folder = "./instance" 
    backup_folder = "./backup"  

    if not os.path.isdir(source_folder):
        logger.info(INFO_SOURCE_FOLDER_MISSING.format(source_folder=source_folder))
        return

    if not os.path.exists(backup_folder):
        try:
            os.makedirs(backup_folder)
            logger.info(INFO_BACKUP_FOLDER_CREATED.format(backup_folder=backup_folder))
        except OSError as e:
            logger.error(INFO_BACKUP_FOLDER_MISSING.format(backup_folder=backup_folder))
            return

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


def backup_data_to_google_drive(logger):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    credentials_path = os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'credentials.json'))
    credentials = Credentials.from_service_account_file(credentials_path)

    drive_service = build('drive', 'v3', credentials=credentials)
    
    backup_folder = "./backup"
    folder_id = "1HKuWr2BcDpXYFEBoL0lcXoApx7jlPgvT"  

    if not os.path.isdir(backup_folder):
        logger.info(INFO_BACKUP_FOLDER_MISSING.format(backup_folder=backup_folder))
        return

    files = sorted(os.listdir(backup_folder), key=lambda x: os.path.getmtime(os.path.join(backup_folder, x)))

    if not files:
        return

    file_name = files[-1]
    source = os.path.join(backup_folder, file_name)
    media = MediaFileUpload(source, resumable=True)
        
    request = drive_service.files().create(
        media_body=media,
        body={
            'name': file_name,
            'parents': [folder_id]
        }
    )
    response = None
        
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                logger.info("Uploaded %d%%." % int(status.progress() * 100))
            logger.info(INFO_BACKUP_UPLOAD_SUCCESS.format(file_name=file_name))
        except Exception as e:
            logger.error(ERROR_BACKUP_UPLOAD_FAILURE.format(file_name=file_name, error=str(e)))
