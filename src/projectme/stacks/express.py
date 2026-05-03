import string
import subprocess

from projectme.utils import fs

# Validation
VALID_CHARS = string.ascii_letters + string.digits + "_-"
VALID_ARGS = {"--rest", "--env"}
VALID_FLAGS = {"--no-git", "--ts", "--docker"}

# Project structures — base JS
BASE_DIRS = ["src"]
BASE_FILES = [
    "package.json",
    ".gitignore",
    "README.md",
    "src/index.js",
]

# Base + --rest (JS)
REST_DIRS = ["src", "src/routes", "src/controllers", "src/middleware"]
REST_FILES = [
    "package.json",
    ".gitignore",
    "README.md",
    "src/index.js",
    "src/routes/index.js",
    "src/controllers/index.js",
    "src/middleware/errorHandler.js",
]

# TypeScript variants
BASE_TS_DIRS = ["src"]
BASE_TS_FILES = [
    "package.json",
    ".gitignore",
    "README.md",
    "tsconfig.json",
    "src/index.ts",
]

REST_TS_DIRS = ["src", "src/routes", "src/controllers", "src/middleware"]
REST_TS_FILES = [
    "package.json",
    ".gitignore",
    "README.md",
    "tsconfig.json",
    "src/index.ts",
    "src/routes/index.ts",
    "src/controllers/index.ts",
    "src/middleware/errorHandler.ts",
]

ENV_FILES = [
    ".env.example",
]

DOCKER_FILES = [
    "Dockerfile",
    ".dockerignore",
]


def _validate(directory: str, arguments: list[str], flags: list[str]):
    for char in directory:
        if char not in VALID_CHARS:
            raise ValueError(f"express.py: build() got an invalid character: '{char}'")
    for arg in arguments:
        if arg not in VALID_ARGS:
            raise ValueError(f"express.py: build() got an unexpected argument: '{arg}'")
    for flag in flags:
        if flag not in VALID_FLAGS:
            raise ValueError(f"express.py: build() got an unexpected flag: '{flag}'")


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


def _pick_scaffold(arguments: list[str], flags: list[str], where: str):
    use_ts = "--ts" in flags
    use_rest = "--rest" in arguments
    use_env = "--env" in arguments
    use_docker = "--docker" in flags

    if use_rest:
        dirs = REST_TS_DIRS if use_ts else REST_DIRS
        files = REST_TS_FILES if use_ts else REST_FILES
    else:
        dirs = BASE_TS_DIRS if use_ts else BASE_DIRS
        files = BASE_TS_FILES if use_ts else BASE_FILES

    if use_env:
        files = files + ENV_FILES

    if use_docker:
        files = files + DOCKER_FILES

    _scaffold(dirs, files, where)


def build(directory: str, where: str, arguments: list[str] = None, flags: list[str] = None):
    if directory is None and where is None:
        raise TypeError("express.py: build() missing 2 required arguments: 'directory' and 'where'")
    if directory is None:
        raise TypeError("express.py: build() missing required argument: 'directory'")
    if where is None:
        raise TypeError("express.py: build() missing required argument: 'where'")

    arguments = arguments or []
    flags = flags or []

    _validate(directory, arguments, flags)

    project_root = fs.mkdir(directory, where)
    _pick_scaffold(arguments, flags, project_root)

    if "--no-git" not in flags:
        _run_git(project_root)

    return project_root
