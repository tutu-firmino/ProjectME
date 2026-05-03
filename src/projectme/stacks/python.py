from projectme.utils import fs

import string
import subprocess

# Validation
VALID_CHARS = string.ascii_letters + string.digits + "_-"
VALID_ARGS = {"--flask", "--django", "--fastapi"}
VALID_FLAGS = {"--no-git", "--no-venv"}

# Bare python project
PYTHON_DIRS  = ["src"]
PYTHON_FILES = [
    "README.md", ".gitignore",
    "src/main.py",
]

# Flask
FLASK_DIRS  = ["src", "src/templates", "src/static"]
FLASK_FILES = [
    "README.md", ".gitignore", "requirements.txt",
    "src/app.py", "src/templates/index.html", "src/static/style.css",
]

# Django
DJANGO_DIRS  = ["src"]
DJANGO_FILES = [
    "README.md", ".gitignore", "requirements.txt", "manage.py",
    "src/settings.py", "src/urls.py", "src/wsgi.py", "src/asgi.py",
]

# FastAPI
FASTAPI_DIRS  = ["src"]
FASTAPI_FILES = [
    "README.md", ".gitignore", "requirements.txt",
    "src/main.py", "src/routes.py", "src/models.py",
]

def _validate(directory: str, arguments: list[str], flags: list[str]):
    for char in directory:
        if char not in VALID_CHARS:
            raise ValueError(f"python.py: build() got an invalid character: '{char}'")
    for arg in arguments:
        if arg not in VALID_ARGS:
            raise ValueError(f"python.py: build() got an unexpected argument: '{arg}'")
    for flag in flags:
        if flag not in VALID_FLAGS:
            raise ValueError(f"python.py: build() got an unexpected flag: '{flag}'")

def _scaffold(dirs: list[str], files: list[str], where: str):
    for folder in dirs:
        fs.mkdir(folder, where)
    for file in files:
        fs.touch(file, where)

def _run_git(directory: str):
    subprocess.run(
        ["git", "init"],
        cwd=directory,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def _run_venv(directory: str):
    subprocess.run(["python", "-m", "venv", ".venv"], cwd=directory)

def _pick_scaffold(arguments: list[str], where: str):
    if "--flask" in arguments:
        _scaffold(FLASK_DIRS, FLASK_FILES, where)
    elif "--django" in arguments:
        _scaffold(DJANGO_DIRS, DJANGO_FILES, where)
    elif "--fastapi" in arguments:
        _scaffold(FASTAPI_DIRS, FASTAPI_FILES, where)
    else:
        _scaffold(PYTHON_DIRS, PYTHON_FILES, where)

def build(directory: str, where: str, arguments: list[str] = None, flags: list[str] = None):
    if directory is None and where is None:
        raise TypeError("python.py: build() missing 2 required arguments: 'directory' and 'where'")
    if directory is None:
        raise TypeError("python.py: build() missing required argument: 'directory'")
    if where is None:
        raise TypeError("python.py: build() missing required argument: 'where'")

    arguments = arguments or []
    flags = flags or []

    _validate(directory, arguments, flags)

    project_root = fs.mkdir(directory, where)
    _pick_scaffold(arguments, project_root)

    if "--no-git" not in flags:
        _run_git(project_root)
    if "--no-venv" not in flags:
        _run_venv(project_root)

    return project_root
