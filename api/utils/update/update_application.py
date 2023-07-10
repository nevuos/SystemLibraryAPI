import os
import requests
import shutil
from api.utils.backup.backup import do_backup
from api.utils.update.github_api import get_latest_release, get_latest_hotfix
from api.utils.update.file_operations import extract_zip_file, write_version_to_file
from api.utils.update.app_operations import get_current_version, restart_application
import filecmp

def get_version_file_path(script_dir):
    return os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'version.txt'))

def download_latest_version(owner, repo, token, script_dir, logger):
    latest_version = get_latest_release(owner, repo, token, logger)
    download_url = f"https://github.com/{owner}/{repo}/archive/{latest_version}.zip"
    zip_file_path = os.path.join(script_dir, 'latest.zip')
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(download_url, headers=headers)
    response.raise_for_status()

    with open(zip_file_path, "wb") as file:
        file.write(response.content)

    return latest_version, zip_file_path

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def download_hotfix_files(owner, repo, token, tag, script_dir):
    release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(release_url, headers=headers)
        response.raise_for_status()
        release = response.json()

        assets = release.get('assets')
        if not assets:
            raise Exception(f"No assets found for the hotfix tag: {tag}")

        temp_dir = os.path.join(script_dir, 'hotfix_temp')
        os.makedirs(temp_dir, exist_ok=True)

        for asset in assets:
            asset_url = asset.get('browser_download_url')
            if asset_url:
                download_file(asset_url, os.path.join(temp_dir, asset['name']))

        return temp_dir
    except requests.exceptions.RequestException as e:
        raise Exception("ERROR_REQUEST_FAILURE") from e

def copy_hotfix_files(hotfix_dir, destination_dir):
    for root, files in os.walk(hotfix_dir):
        for file in files:
            if not file.endswith('.py'):  # Only copy Python files
                continue

            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, hotfix_dir)
            destination_path = os.path.join(destination_dir, relative_path)

            if os.path.exists(destination_path) and filecmp.cmp(source_path, destination_path):
                continue

            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy2(source_path, destination_path)

def update_application(logger):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    owner = "nevuos"
    repo = "SystemLibraryAPI"
    token = os.getenv("GITHUB_TOKEN")

    try:
        logger.info("Checking for updates...")
        current_version = get_current_version(get_version_file_path(script_dir))
        latest_version = get_latest_release(owner, repo, token, logger)

        if latest_version == current_version:
            logger.info("INFO_UP_TO_DATE")
            return

        logger.info("Update found. Backing up the database before updating...")
        # Backup the database before updating
        do_backup(logger)
        
        # Check if the latest tag is a hotfix tag
        is_hotfix = latest_version.startswith("hotfix")

        if is_hotfix:
            logger.info("Applying hotfix...")

            # Get the latest hotfix tag
            hotfix_tag = get_latest_hotfix(owner, repo, token, logger)

            # Download only the hotfix files based on the tag
            hotfix_dir = download_hotfix_files(owner, repo, token, hotfix_tag, script_dir)

            # Copy the hotfix files to the project folder, replacing existing ones if necessary
            copy_hotfix_files(hotfix_dir, script_dir)

            # Remove the temporary hotfix folder
            shutil.rmtree(hotfix_dir)

            logger.info("Restarting application...")
            # Restart the application
            restart_application(os.path.join(script_dir, '__init__.py'), logger)

            logger.info("Hotfix applied!")

            # Check the version again after applying the hotfix
            current_version = get_current_version(get_version_file_path(script_dir))
            latest_version = get_latest_release(owner, repo, token, logger)

            if latest_version == current_version:
                logger.info("INFO_UP_TO_DATE")
                return
            elif latest_version.startswith("hotfix"):
                logger.error("ERROR_HOTFIX_NOT_APPLIED")
                return

        current_version = get_current_version(get_version_file_path(script_dir))
        latest_version, zip_file_path = download_latest_version(owner, repo, token, script_dir, logger)

        if latest_version == current_version:
            logger.info("INFO_UP_TO_DATE")
            return

        logger.info("Downloading latest version...")
        # Extract the ZIP file to the project folder
        extract_zip_file(zip_file_path, script_dir)

        # Write the updated version to the version.txt file
        write_version_to_file(latest_version, get_version_file_path(script_dir))

        # Remove the ZIP file
        os.remove(zip_file_path)

        logger.info("Restarting application...")
        # Restart the application
        restart_application(os.path.join(script_dir, '__init__.py'), logger)

        logger.info("Update successful!")

    except requests.exceptions.RequestException:
        logger.error("ERROR_NO_INTERNET")
    except Exception as e:
        logger.error("ERROR_REQUEST_FAILURE: " + str(e))
        logger.error("ERROR_CODE_UPDATE_FAILURE")
