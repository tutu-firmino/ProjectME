<div align="center">

![logo](https://github.com/tutu-firmino/ProjectME/blob/master/assets/logo.svg)

**Scaffold React, Next.js, Express, and Python projects — in seconds.**

[![Version](https://img.shields.io/badge/version-0.4.0-bright_green)](https://github.com/tutu-firmino/ProjectME/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

---

ProjectME is a CLI tool that generates clean, production-ready project structures from the command line. Pick your stack, pass a few flags, and start coding — or define your entire project in a `.projectme` manifest file.

Every generated project includes a standard directory layout, a `README.md`, a `.gitignore`, and Git initialization. Python projects also get a virtual environment by default.

> **Note:** Both `projectme create ...` and `project create ...` work as commands.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Supported Stacks](#supported-stacks)
- [Options & Flags](#options--flags)
- [Manifest File](#manifest-file)
- [Documentation](#documentation)
- [Contributing & Feedback](#contributing--feedback)
- [License](#license)

---

## Installation

Requires Python 3.10+.

```bash
pip install projectme
```

<details>
<summary>Install from source</summary>

```bash
git clone https://github.com/tutu-firmino/ProjectME.git
cd ProjectME
pip install -e .
```

With development dependencies:

```bash
pip install -e .[test,lint,build]
```

</details>

---

## Quick Start

```bash
# React app (Vite)
projectme create my-app react

# Next.js app with Tailwind CSS
projectme create my-app nextjs --tailwind

# Express REST API with TypeScript
projectme create my-server express --rest --ts

# Python API with FastAPI
projectme create my-api python --fastapi
```

Options can be freely combined:

```bash
projectme create my-app nextjs --tailwind --src --eslint
projectme create my-server express --rest --ts --docker --env
```

---

## Supported Stacks

| Stack | Default setup | Notable options |
|-------|--------------|-----------------|
| `react` | Vite | `--cra`, `--tailwind` |
| `nextjs` | App Router, TypeScript | `--tailwind`, `--src`, `--pages-router`, `--eslint`, `--turbopack`, `--js` |
| `express` | Bare JavaScript | `--rest`, `--ts`, `--docker`, `--env` |
| `python` | Bare project + virtualenv | `--flask`, `--django`, `--fastapi`, `--no-venv` |

All stacks support `--no-git` to skip `git init`.

---

## Options & Flags

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

ProjectME validates all flags against the chosen stack before creating any files. Incompatible combinations produce a clear error, for example:

```
--flask cannot be used with the react stack
```

---

## Manifest File

For complex or reproducible setups, define your project in a `.projectme` TOML file and run:

```bash
projectme read_manifest
```

### Example manifest

```toml
[project]
name = "my-app"         # required
stack = "nextjs"        # required — one of: react, nextjs, express, python
where = "/path/to/dir"  # optional — defaults to current directory

[args]
tailwind = true
eslint = true

[flags]
turbopack = false
no-git = false

[meta]
author = "your-name"
version = "1.0.0"
description = "My project"
```

The manifest is fully validated before any files are created — missing required keys, unknown sections, type mismatches, and invalid stack names all produce descriptive errors.

For the full manifest schema and all available keys, see [DOCUMENTATION.md](DOCUMENTATION.md#manifest-files).

---

## Documentation

Full CLI reference, per-stack file trees, manifest schema, architecture overview, and development guide are all in [DOCUMENTATION.md](DOCUMENTATION.md).

---

## Contributing & Feedback

Contributions, bug reports, and feature suggestions are welcome! Feel free to open an issue or start a discussion on the [GitHub repository](https://github.com/tutu-firmino/ProjectME).

---

## License

Distributed under the [MIT License](LICENSE).