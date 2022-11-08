import shutil
import zipfile

from os import mkdir


def unzipper(filepath, extract_path):
    try:
        mkdir(extract_path)
    except FileExistsError:
        shutil.rmtree(extract_path)
        mkdir(extract_path)

    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(extract_path)


def cleanup():
    shutil.rmtree("./unzipped")
    shutil.rmtree("./files")
