from pathlib import Path

import tomllib

from projectme.stacks import express, nextjs, python, react
from projectme.utils import fs

MANIFEST_SCHEMA = {
    "project": {
        "_required": True,
        "name": {"type": str, "required": True},
        "stack": {"type": str, "required": True},
        "where": {"type": str, "required": False},
    },
    "args": {
        "_required": False,
        "tailwind": {"type": bool, "required": False},
        "cra": {"type": bool, "required": False},
        "flask": {"type": bool, "required": False},
        "django": {"type": bool, "required": False},
        "fastapi": {"type": bool, "required": False},
        "eslint": {"type": bool, "required": False},
        "pages-router": {"type": bool, "required": False},
        "src": {"type": bool, "required": False},
        "rest": {"type": bool, "required": False},
        "env": {"type": bool, "required": False},
    },
    "flags": {
        "_required": False,
        "no-git": {"type": bool, "required": False},
        "no-venv": {"type": bool, "required": False},
        "turbopack": {"type": bool, "required": False},
        "js": {"type": bool, "required": False},
        "ts": {"type": bool, "required": False},
        "docker": {"type": bool, "required": False},
    },
    "meta": {
        "_required": False,
        "author": {"type": str, "required": False},
        "version": {"type": str, "required": False},
        "description": {"type": str, "required": False},
    },
}
VALID_STACKS = {"react", "python", "nextjs", "express"}


def _search_manifest(path: Path | None = None) -> dict:
    search_dir = fs.resolve(path) if path else fs.cwd()
    manifest_file = fs.resolve(search_dir / ".projectme")

    if not manifest_file.exists():
        raise FileNotFoundError("manifest.py: no .projectme file found in the current directory")

    with open(manifest_file, "rb") as f:
        return tomllib.load(f)


def _validate_manifest(data: dict):
    for section in data:
        if section not in MANIFEST_SCHEMA:
            raise ValueError(f"manifest.py: unknown section '[{section}]'")

    for section, schema in MANIFEST_SCHEMA.items():
        is_required = schema["_required"]
        present = section in data

        if is_required and not present:
            raise ValueError(f"manifest.py: missing required section '[{section}]'")
        if not present:
            continue

        block = data[section]

        known_keys = {k for k in schema if k != "_required"}
        for key in block:
            if key not in known_keys:
                raise ValueError(f"manifest.py: '[{section}]' has unknown key '{key}'")

        for key, rules in schema.items():
            if key == "_required":
                continue
            if rules["required"] and key not in block:
                raise ValueError(f"manifest.py: '[{section}]' is missing required key '{key}'")
            if key in block and not isinstance(block[key], rules["type"]):
                expected = rules["type"].__name__
                got = type(block[key]).__name__
                raise ValueError(f"manifest.py: '[{section}].{key}' expected {expected}, got {got}")

    stack = data.get("project", {}).get("stack")
    if stack and stack not in VALID_STACKS:
        raise ValueError(
            f"manifest.py: unknown stack '{stack}', valid stacks are: {', '.join(sorted(VALID_STACKS))}"
        )


def read_and_build(path: Path | None = None) -> dict:
    data = _search_manifest(path)
    _validate_manifest(data)

    project = data["project"]
    args = data.get("args", {})
    flags = data.get("flags", {})

    name = project["name"]
    stack = project["stack"]
    where = project.get("where", str(fs.cwd()))

    arg_list = [f"--{k}" for k, v in args.items() if v]
    flag_list = [f"--{k}" for k, v in flags.items() if v]

    # Import and call the right builder
    if stack == "react":
        react.build(name, where, arg_list, flag_list)
    elif stack == "nextjs":
        nextjs.build(name, where, arg_list, flag_list)
    elif stack == "express":
        express.build(name, where, arg_list, flag_list)
    elif stack == "python":
        python.build(name, where, arg_list, flag_list)

    return {"name": name, "stack": stack, "where": where,
            "flags": flag_list, "args": arg_list}
