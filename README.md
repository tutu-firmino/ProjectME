# ProjectME

[![Version](https://img.shields.io/badge/version-0.3.0-bright_green)](https://github.com/tutu-firmino/ProjectME/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> A CLI for scaffolding Python and React projects.

ProjectME generates clean, ready-to-use project structures from the command line. Pick your stack, pass a few flags, and start coding.

---

## Installation

```bash
pip install projectme
```

Or install it from source in editable mode:

```bash
git clone https://github.com/tutu-firmino/ProjectME.git
cd ProjectME
pip install -e .
```

---

## Usage

> NOTE: Both commands `projectme create...` and `project create...` work.


### Create a React project

```bash
projectme create my-app react
```

With Tailwind CSS:

```bash
projectme create my-app react --tailwind
```

Using Create React App instead of Vite:

```bash
projectme create my-app react --cra
```

### Create a Python project

```bash
projectme create my-service python
```

With a web framework:

```bash
projectme create my-api python --fastapi
projectme create my-site python --flask
projectme create my-project python --django
```

Skip Git initialization or virtual environment creation:

```bash
projectme create my-service python --no-git --no-venv
```

### Global options

| Option       | Description                                       |
|--------------|---------------------------------------------------|
| `--tailwind` | Add Tailwind CSS (React only)                     |
| `--cra`      | Use Create React App instead of Vite (React only) |
| `--flask`    | Scaffold a Flask project (Python only)            |
| `--django`   | Scaffold a Django project (Python only)           |
| `--fastapi`  | Scaffold a FastAPI project (Python only)          |
| `--no-git`   | Skip `git init`                                   |
| `--no-venv`  | Skip virtual environment creation (Python only)   |

---

## Development

Install development dependencies:

```bash
pip install -e .[test,lint,build]
```

Run the test suite:

```bash
pytest
```

Run the linter:

```bash
ruff check .
ruff format --check .
```

Build and upload:

```bash
python -m build
twine upload dist/*
```

---

## Roadmap

> We are currently on version **v0.3.0**.

**Upcoming features**

- (guaranteed) **v0.4.0**: in addition to more available stacks, a new manifest file feature will come.
- (planned) **v0.5.0**: AI-powered smart committing tool
- (guaranteed) **v1.0.0**: complete coverage and project stabilization

---

## License

[MIT](LICENSE)

---

## Feedback

We welcome feedback and suggestions to help improve the project. Thank you!