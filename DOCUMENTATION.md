# ProjectME Documentation

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [CLI Reference](#cli-reference)
- [Stacks](#stacks)
  - [React](#react)
  - [Python](#python)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Releasing](#releasing)

---

## Overview

ProjectME is a command-line tool that generates boilerplate code for Python and React projects. It focuses on speed and simplicity: run a single command and get a working project skeleton with sensible defaults.

Supported stacks:
- **React** (Vite by default, optional Create React App and Tailwind CSS)
- **Python** (bare project by default, optional Flask, Django, or FastAPI)

All projects include:
- A standard directory layout
- A `README.md`
- A `.gitignore`
- Git initialization (unless `--no-git` is passed)

Python projects also get a virtual environment by default (unless `--no-venv` is passed).

---

## Installation

### From PyPI

```bash
pip install projectme
```

### From source

```bash
git clone https://github.com/tutu-firmino/ProjectME.git
cd ProjectME
pip install -e .
```

### Development dependencies

```bash
pip install -e .[test,lint,build]
```

---

## CLI Reference

### `projectme create`

Create a new project.

```text
projectme create NAME STACK [OPTIONS]
```

**Arguments:**

| Argument | Description                            |
|----------|----------------------------------------|
| `NAME`   | Project name (used for the directory)  |
| `STACK`  | Project stack: `python` or `react`     |

**Options:**

| Option       | Stack  | Description                              |
|--------------|--------|------------------------------------------|
| `--tailwind` | React  | Include Tailwind CSS configuration files |
| `--cra`      | React  | Use Create React App instead of Vite     |
| `--flask`    | Python | Scaffold a Flask application             |
| `--django`   | Python | Scaffold a Django application            |
| `--fastapi`  | Python | Scaffold a FastAPI application           |
| `--no-git`   | Both   | Skip Git repository initialization       |
| `--no-venv`  | Python | Skip Python virtual environment creation |

**Validation:**

ProjectME validates that flags match the selected stack. For example, passing `--flask` with the `react` stack results in an error:

```text
--flask cannot be used with the react stack
```

---

## Stacks

### React

#### Default (Vite)

```bash
projectme create my-app react
```

Generated files:

```
my-app/
├── index.html
├── vite.config.js
├── package.json
├── .gitignore
├── README.md
├── public/
│   └── vite.svg
└── src/
    ├── App.jsx
    ├── main.jsx
    ├── App.css
    └── index.css
```

#### With Tailwind CSS

```bash
projectme create my-app react --tailwind
```

Adds:

```
my-app/
├── tailwind.config.js
└── postcss.config.js
```

#### With Create React App

```bash
projectme create my-app react --cra
```

Generated files:

```
my-app/
├── package.json
├── .gitignore
├── README.md
├── public/
│   ├── index.html
│   ├── favicon.ico
│   ├── manifest.json
│   └── robots.txt
└── src/
    ├── App.js
    ├── App.css
    ├── App.test.js
    ├── index.js
    ├── index.css
    ├── reportWebVitals.js
    └── setupTests.js
```

### Python

#### Default (bare project)

```bash
projectme create my-project python
```

Generated files:

```
my-project/
├── README.md
├── .gitignore
└── src/
    └── main.py
```

#### With Flask

```bash
projectme create my-app python --flask
```

Generated files:

```
my-app/
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
```

#### With Django

```bash
projectme create my-site python --django
```

Generated files:

```
my-site/
├── README.md
├── .gitignore
├── requirements.txt
├── manage.py
└── src/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

#### With FastAPI

```bash
projectme create my-api python --fastapi
```

Generated files:

```
my-api/
├── README.md
├── .gitignore
├── requirements.txt
└── src/
    ├── main.py
    ├── routes.py
    └── models.py
```

---

## Project Structure

```
ProjectME/
├── src/
│   └── projectme/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── core/
│       │   ├── __init__.py
│       │   └── scaffold.py      # Core scaffolding dispatcher
│       ├── stacks/
│       │   ├── __init__.py
│       │   ├── python.py        # Python stack builder
│       │   └── react.py         # React stack builder
│       └── utils/
│           ├── __init__.py
│           └── fs.py            # Filesystem helpers
├── tests/
│   ├── test_cli.py
│   └── test_scaffold.py
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Development Guide

### Running tests

```bash
pytest
```

The test suite covers:
- CLI invocation and exit codes
- Correct file generation for each stack
- Argument validation
- Git and virtual environment behavior
- Subprocess mocking for isolation

Coverage is enforced at **90%**.

### Linting

This project uses **Ruff** for linting and formatting.

```bash
# Check code
ruff check .

# Check formatting
ruff format --check .

# Auto-fix issues
ruff check . --fix

# Auto-format
ruff format .
```

### Type checking

ProjectME uses Python type hints throughout. To verify:

```bash
python -m mypy src
```

*(mypy is not included as a project dependency; install it separately if needed.)*

---

## Architecture

### Entry Point

`projectme.main` defines the Typer CLI application. Commands are registered with `@cli.command()`, and options use `Annotated` types for clean signatures.

### Scaffolding Flow

1. **CLI Layer** (`main.py`): Parses arguments, validates stack-specific options, and calls `scaffold()`.
2. **Core Layer** (`core/scaffold.py`): Validates required arguments and dispatches to the correct stack builder.
3. **Stack Layer** (`stacks/python.py`, `stacks/react.py`): Builds the concrete file tree and runs optional setup commands (Git init, virtualenv).
4. **Utility Layer** (`utils/fs.py`): Provides thin wrappers around `pathlib` for directory and file creation.

### Validation

Stack-specific options are validated before any files are created. This prevents partial or broken projects if incompatible flags are passed.

### Extensibility

To add a new stack:

1. Create a new module under `src/projectme/stacks/` (e.g., `svelte.py`).
2. Implement a `build(directory, where, arguments, flags)` function.
3. Register the stack in `core/scaffold.py`:
```python
STACK_BUILDERS = {
    "react": react.build,
    "python": python.build,
    "svelte": svelte.build,
}
```
4. Add the stack to the `Stack` enum in `main.py`.

---

## Configuration

ProjectME behavior is controlled entirely through CLI flags. There is no configuration file.

### Python version support

ProjectME requires Python **3.10 or later**.

---

## Releasing

1. Update the version in `pyproject.toml`.
2. Ensure all tests pass. (obviously)
3. Build the distribution:
```bash
python -m build
```
4. Upload to PyPI:
```bash
twine upload dist/*
```
5. Tag the release:
```bash
git tag v$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
git push origin --tags
```
