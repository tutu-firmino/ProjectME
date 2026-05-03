import string
import subprocess

from projectme.utils import fs

# Validation
VALID_CHARS = string.ascii_letters + string.digits + "_-"
VALID_ARGS = {"--tailwind", "--src", "--pages-router", "--eslint"}
VALID_FLAGS = {"--no-git", "--turbopack", "--js"}

# Project structures — App Router
NEXT_DIRS = ["app", "public"]
NEXT_FILES = [
    "next.config.js",
    "package.json",
    ".gitignore",
    "README.md",
    "tsconfig.json",
    "app/layout.tsx",
    "app/page.tsx",
    "app/globals.css",
    "public/next.svg",
    "public/vercel.svg",
]

# App Router + --src-dir
SRC_DIRS = ["src/app", "public"]
SRC_FILES = [
    "next.config.js",
    "package.json",
    ".gitignore",
    "README.md",
    "tsconfig.json",
    "src/app/layout.tsx",
    "src/app/page.tsx",
    "src/app/globals.css",
    "public/next.svg",
    "public/vercel.svg",
]

# Pages Router
PAGES_DIRS = ["pages", "public", "styles"]
PAGES_FILES = [
    "next.config.js",
    "package.json",
    ".gitignore",
    "README.md",
    "tsconfig.json",
    "pages/_app.tsx",
    "pages/_document.tsx",
    "pages/index.tsx",
    "styles/globals.css",
    "styles/Home.module.css",
    "public/next.svg",
    "public/vercel.svg",
]

# Pages Router + --src-dir
PAGES_SRC_DIRS = ["src/pages", "public", "src/styles"]
PAGES_SRC_FILES = [
    "next.config.js",
    "package.json",
    ".gitignore",
    "README.md",
    "tsconfig.json",
    "src/pages/_app.tsx",
    "src/pages/_document.tsx",
    "src/pages/index.tsx",
    "src/styles/globals.css",
    "src/styles/Home.module.css",
    "public/next.svg",
    "public/vercel.svg",
]

TAILWIND_FILES = [
    "tailwind.config.ts",
    "postcss.config.js",
]

ESLINT_FILES = [
    ".eslintrc.json",
]


def _validate(directory: str, arguments: list[str], flags: list[str]):
    for char in directory:
        if char not in VALID_CHARS:
            raise ValueError(f"nextjs.py: build() got an invalid character: '{char}'")
    for arg in arguments:
        if arg not in VALID_ARGS:
            raise ValueError(f"nextjs.py: build() got an unexpected argument: '{arg}'")
    for flag in flags:
        if flag not in VALID_FLAGS:
            raise ValueError(f"nextjs.py: build() got an unexpected flag: '{flag}'")


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


def _to_js(files: list[str]) -> list[str]:
    result = []
    for file in files:
        if file.endswith(".tsx"):
            result.append(file[:-4] + ".jsx")
        elif file.endswith(".ts") and not file.endswith("tsconfig.json"):
            result.append(file[:-3] + ".js")
        else:
            result.append(file)
    return [f for f in result if f != "tsconfig.json"]


def _pick_scaffold(arguments: list[str], flags: list[str], where: str):
    use_pages = "--pages-router" in arguments
    use_src = "--src" in arguments
    use_js = "--js" in flags

    if use_pages:
        dirs = PAGES_SRC_DIRS if use_src else PAGES_DIRS
        files = PAGES_SRC_FILES if use_src else PAGES_FILES
    else:
        dirs = SRC_DIRS if use_src else NEXT_DIRS
        files = SRC_FILES if use_src else NEXT_FILES

    if use_js:
        files = _to_js(files)

    if "--tailwind" in arguments:
        tailwind = TAILWIND_FILES
        if use_js:
            tailwind = _to_js(tailwind)
        files = files + tailwind

    if "--eslint" in arguments:
        files = files + ESLINT_FILES

    _scaffold(dirs, files, where)


def build(directory: str, where: str, arguments: list[str] = None, flags: list[str] = None):
    if directory is None and where is None:
        raise TypeError("nextjs.py: build() missing 2 required arguments: 'directory' and 'where'")
    if directory is None:
        raise TypeError("nextjs.py: build() missing required argument: 'directory'")
    if where is None:
        raise TypeError("nextjs.py: build() missing required argument: 'where'")

    arguments = arguments or []
    flags = flags or []

    _validate(directory, arguments, flags)

    project_root = fs.mkdir(directory, where)
    _pick_scaffold(arguments, flags, project_root)

    if "--no-git" not in flags:
        _run_git(project_root)

    return project_root
