from pathlib import Path


def cwd():
    return Path.cwd()


def parent():
    return cwd().parent


def resolve(path):
    return Path(path).resolve()


def mkdir(dir_name: str, where: str):
    directory = Path(where).joinpath(dir_name).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def touch(file_name: str, where: str):
    file = Path(where).joinpath(file_name).resolve()
    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch(exist_ok=True)
    return file
