# ProjectME Documentation

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [CLI Reference](#cli-reference)
- [Manifest Files](#manifest-files)
- [Stacks](#stacks)
  - [React](#react)
  - [Next.js](#nextjs)
  - [Express](#express)
  - [Python](#python)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Architecture](#architecture)
- [Releasing](#releasing)

---

## Overview

ProjectME is a command-line tool that scaffolds boilerplate for React, Next.js, Express, and Python projects. Run a single command and get a working project skeleton with sensible defaults — no manual setup, no copy-pasting.

**Supported stacks:**

- **React** — Vite by default, optional Create React App and Tailwind CSS
- **Next.js** — App Router by default, optional Pages Router, Tailwind CSS, ESLint, Turbopack, and more
- **Express** — bare by default, optional REST boilerplate, TypeScript, Docker, and env files
- **Python** — bare project by default, optional Flask, Django, or FastAPI

Every generated project includes a standard directory layout, a `README.md`, a `.gitignore`, and Git initialization (skip with `--no-git`). Python projects also get a virtual environment by default (skip with `--no-venv`).

> **Note:** Both `projectme create ...` and `project create ...` work as commands.

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

### With development dependencies

```bash
pip install -e .[test,lint,build]
```

Requires **Python 3.10 or later**.

---

## CLI Reference

### `projectme create`

Creates a new project in a new directory.

```
projectme create NAME STACK [OPTIONS]
```

| Argument | Description |
|----------|-------------|
| `NAME` | Project name, used as the output directory name |
| `STACK` | One of: `react`, `nextjs`, `express`, `python` |

**All options:**

| Option | Applies to | Description |
|--------|------------|-------------|
| `--tailwind` | React, Next.js | Add Tailwind CSS configuration |
| `--cra` | React | Use Create React App instead of Vite |
| `--src` | Next.js | Place `app/` under a `src/` directory |
| `--pages-router` | Next.js | Use Pages Router instead of App Router |
| `--eslint` | Next.js | Include ESLint configuration |
| `--turbopack` | Next.js | Enable Turbopack |
| `--js` | Next.js | Use JavaScript instead of TypeScript |
| `--rest` | Express | Include REST boilerplate (routes, controllers, middleware) |
| `--env` | Express | Include a `.env.example` file |
| `--ts` | Express | Use TypeScript |
| `--docker` | Express | Include `Dockerfile` and `.dockerignore` |
| `--flask` | Python | Scaffold a Flask application |
| `--django` | Python | Scaffold a Django application |
| `--fastapi` | Python | Scaffold a FastAPI application |
| `--no-git` | All | Skip `git init` |
| `--no-venv` | Python | Skip virtual environment creation |

**Validation:** ProjectME checks that all flags are compatible with the chosen stack before creating any files. For example, passing `--flask` with the `react` stack will produce an error like:

```
--flask cannot be used with the react stack
```

---

### `projectme read_manifest`

Builds a project from a `.projectme` manifest file in the current directory.

```
projectme read_manifest
```

Reads and validates the manifest, then invokes the appropriate stack builder. See [Manifest Files](#manifest-files) for the file format.

---

## Manifest Files

Instead of passing all options on the command line every time, you can define a project in a `.projectme` TOML file and run `projectme read` to build it.

### File format

```toml
[project]
name = "my-app"         # required — project name
stack = "react"         # required — one of: react, nextjs, express, python
where = "/path/to/dir"  # optional — output directory (defaults to current directory)

[args]
tailwind = true         # stack-specific arguments (all optional, type: bool)
eslint = true

[flags]
no-git = true           # stack-specific flags (all optional, type: bool)
turbopack = false

[meta]
author = "your-name"       # optional metadata
version = "1.0.0"
description = "My project"
```

### Available `[args]` keys

| Key | Applies to |
|-----|------------|
| `tailwind` | React, Next.js |
| `cra` | React |
| `eslint` | Next.js |
| `pages-router` | Next.js |
| `src` | Next.js |
| `rest` | Express |
| `env` | Express |
| `flask` | Python |
| `django` | Python |
| `fastapi` | Python |

### Available `[flags]` keys

| Key | Applies to |
|-----|------------|
| `no-git` | All |
| `no-venv` | Python |
| `turbopack` | Next.js |
| `js` | Next.js |
| `ts` | Express |
| `docker` | Express |

### Validation

The manifest is fully validated before any files are created. Errors are raised for:

- Missing `[project]` section or required keys (`name`, `stack`)
- Unknown sections or keys
- Incorrect value types (e.g. a string where a boolean is expected)
- Invalid stack name

---

## Stacks

### React

#### Default (Vite)

```bash
projectme create my-app react
```

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

#### With Tailwind CSS (`--tailwind`)

Adds `tailwind.config.js` and `postcss.config.js` to the project root.

#### With Create React App (`--cra`)

```bash
projectme create my-app react --cra
```

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

---

### Next.js

#### Default (App Router, TypeScript)

```bash
projectme create my-app nextjs
```

```
my-app/
├── next.config.js
├── package.json
├── tsconfig.json
├── .gitignore
├── README.md
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
└── public/
    ├── next.svg
    └── vercel.svg
```

#### With `src/` directory (`--src`)

Moves `app/` under `src/app/`.

#### Pages Router (`--pages-router`)

```bash
projectme create my-app nextjs --pages-router
```

```
my-app/
├── next.config.js
├── package.json
├── tsconfig.json
├── .gitignore
├── README.md
├── pages/
│   ├── _app.tsx
│   ├── _document.tsx
│   └── index.tsx
├── styles/
│   ├── globals.css
│   └── Home.module.css
└── public/
    ├── next.svg
    └── vercel.svg
```

#### With Tailwind CSS (`--tailwind`)

Adds `tailwind.config.ts` and `postcss.config.js`.

#### With JavaScript (`--js`)

Replaces all `.tsx`/`.ts` files with `.jsx`/`.js` equivalents and removes `tsconfig.json`.

#### Combining options

Options can be freely combined:

```bash
projectme create my-app nextjs --tailwind --src --eslint
projectme create my-app nextjs --pages-router --js
```

---

### Express

#### Default (JavaScript)

```bash
projectme create my-server express
```

```
my-server/
├── package.json
├── .gitignore
├── README.md
└── src/
    └── index.js
```

#### With REST boilerplate (`--rest`)

```bash
projectme create my-server express --rest
```

Adds structured routing:

```
my-server/
└── src/
    ├── index.js
    ├── routes/
    │   └── index.js
    ├── controllers/
    │   └── index.js
    └── middleware/
        └── errorHandler.js
```

#### With TypeScript (`--ts`)

Replaces `.js` files with `.ts` equivalents and adds `tsconfig.json`.

#### With Docker (`--docker`)

Adds `Dockerfile` and `.dockerignore` to the project root.

#### With env file (`--env`)

Adds `.env.example` to the project root.

#### Combining options

```bash
projectme create my-server express --rest --ts --docker --env
```

---

### Python

#### Default (bare project)

```bash
projectme create my-project python
```

```
my-project/
├── README.md
├── .gitignore
└── src/
    └── main.py
```

A virtual environment is created automatically unless `--no-venv` is passed.

#### With Flask (`--flask`)

```bash
projectme create my-app python --flask
```

```
my-app/
├── README.md
├── .gitignore
├── requirements.txt
└── src/
    ├── app.py
    ├── templates/
    │   └── index.html
    └── static/
        └── style.css
```

#### With Django (`--django`)

```bash
projectme create my-site python --django
```

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

#### With FastAPI (`--fastapi`)

```bash
projectme create my-api python --fastapi
```

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

#### Skipping Git or virtualenv

```bash
projectme create my-service python --no-git --no-venv
```

---

## Project Structure

```
ProjectME/
├── src/
│   └── projectme/
│       ├── __init__.py
│       ├── main.py              # CLI entry point (Typer app)
│       ├── core/
│       │   ├── __init__.py
│       │   ├── manifest.py      # .projectme file reader and validator
│       │   └── scaffold.py      # Scaffolding dispatcher
│       ├── stacks/
│       │   ├── __init__.py
│       │   ├── express.py       # Express builder
│       │   ├── nextjs.py        # Next.js builder
│       │   ├── python.py        # Python builder
│       │   └── react.py         # React builder
│       └── utils/
│           ├── __init__.py
│           └── fs.py            # Filesystem helpers (pathlib wrappers)
├── tests/
│   ├── test_cli.py
│   ├── test_manifest.py
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

The test suite covers CLI invocation and exit codes, correct file generation per stack, argument and flag validation, manifest reading and building, and Git/virtualenv behavior. Coverage is enforced at **90%**.

### Linting and formatting

ProjectME uses [Ruff](https://github.com/astral-sh/ruff) for both linting and formatting.

```bash
# Check for issues
ruff check .

# Check formatting
ruff format --check .

# Auto-fix issues
ruff check . --fix

# Auto-format
ruff format .
```

### Type checking

Type hints are used throughout the codebase. To verify with mypy (install separately):

```bash
python -m mypy src
```

---

## Architecture

### How a project gets built

1. **CLI layer** (`main.py`): Parses arguments using Typer, validates stack-specific flag combinations, then calls `scaffold()`.
2. **Core layer** (`core/scaffold.py`): Validates required arguments and dispatches to the correct stack builder.
3. **Manifest layer** (`core/manifest.py`): Reads `.projectme` TOML files, validates the schema, and dispatches to the stack builder — used by `projectme read`.
4. **Stack layer** (`stacks/*.py`): Each module builds the concrete file tree and runs optional setup commands (Git init, virtualenv creation).
5. **Utility layer** (`utils/fs.py`): Thin wrappers around `pathlib` for consistent directory and file creation.

### Adding a new stack

1. Create `src/projectme/stacks/svelte.py` (or whichever stack name).
2. Implement a `build(directory, where, arguments, flags)` function.
3. Register it in `core/scaffold.py`:

```python
STACK_BUILDERS = {
    "react": react.build,
    "python": python.build,
    "nextjs": nextjs.build,
    "express": express.build,
    "ruby_on_rails": ruby_on_rails.build,  # new
}
```

4. Add the stack name to the `Stack` enum in `main.py`.
5. Add it to `VALID_STACKS` in `core/manifest.py`.

---

## Releasing

1. Update the version in `pyproject.toml`.
2. Make sure all tests pass.
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