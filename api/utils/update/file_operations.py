import zipfile

def extract_zip_file(zip_file_path, extract_to):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

def write_version_to_file(version, file_path):
    with open(file_path, "w") as file:
        file.write(version)
