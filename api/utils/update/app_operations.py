import subprocess
import platform

def get_current_version(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

def restart_application(init_file_path, logger):
    operating_system = platform.system()

    if operating_system == "Windows":
        logger.info("Restarting application...")
        subprocess.call(["python3", init_file_path])
    elif operating_system == "Linux":
        logger.info("Restarting application...")
        subprocess.call(["sudo", "python3", init_file_path])
    else:
        logger.error("ERROR_UNSUPPORTED_OS")
