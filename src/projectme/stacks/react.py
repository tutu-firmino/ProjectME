import string
import subprocess

from projectme.utils import fs

# Validation
VALID_CHARS = string.ascii_letters + string.digits + "_-"
VALID_ARGS = {"--tailwind", "--cra"}
VALID_FLAGS = {"--no-git"}

# Project structures
VITE_DIRS = ["src", "public"]
VITE_FILES = [
    "index.html",
    "vite.config.js",
    "package.json",
    ".gitignore",
    "README.md",
    "src/App.jsx",
    "src/main.jsx",
    "src/App.css",
    "src/index.css",
    "public/vite.svg",
]

CRA_DIRS = ["src", "public"]
CRA_FILES = [
    "package.json",
    ".gitignore",
    "README.md",
    "src/App.js",
    "src/App.css",
    "src/App.test.js",
    "src/index.js",
    "src/index.css",
    "src/reportWebVitals.js",
    "src/setupTests.js",
    "public/index.html",
    "public/favicon.ico",
    "public/manifest.json",
    "public/robots.txt",
]

TAILWIND_FILES = [
    "tailwind.config.js",
    "postcss.config.js",
]


def _validate(directory: str, arguments: list[str], flags: list[str]):
    for char in directory:
        if char not in VALID_CHARS:
            raise ValueError(f"react.py: build() got an invalid character: '{char}'")
    for arg in arguments:
        if arg not in VALID_ARGS:
            raise ValueError(f"react.py: build() got an unexpected argument: '{arg}'")
    for flag in flags:
        if flag not in VALID_FLAGS:
            raise ValueError(f"react.py: build() got an unexpected flag: '{flag}'")


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


def _pick_scaffold(arguments: list[str], where: str):
    if "--cra" in arguments:
        if "--tailwind" in arguments:
            _scaffold(CRA_DIRS, CRA_FILES + TAILWIND_FILES, where)
        else:
            _scaffold(CRA_DIRS, CRA_FILES, where)
    elif "--tailwind" in arguments:
        _scaffold(VITE_DIRS, VITE_FILES + TAILWIND_FILES, where)
    else:
        _scaffold(VITE_DIRS, VITE_FILES, where)


def build(directory: str, where: str, arguments: list[str] = None, flags: list[str] = None):
    if directory is None and where is None:
        raise TypeError("react.py: build() missing 2 required arguments: 'directory' and 'where'")
    if directory is None:
        raise TypeError("react.py: build() missing required argument: 'directory'")
    if where is None:
        raise TypeError("react.py: build() missing required argument: 'where'")

    arguments = arguments or []
    flags = flags or []

    _validate(directory, arguments, flags)

    project_root = fs.mkdir(directory, where)
    _pick_scaffold(arguments, project_root)

    if "--no-git" not in flags:
        _run_git(project_root)

    return project_root
