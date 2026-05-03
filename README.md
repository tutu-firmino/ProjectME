# ProjectME

[![Version](https://img.shields.io/badge/version-0.4.0-bright_green)](https://github.com/tutu-firmino/ProjectME/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![logo](https://github.com/tutu-firmino/ProjectME/blob/master/assets/logo.svg)

> A CLI for scaffolding React, Next.js, Express, and Python projects.

ProjectME generates clean, ready-to-use project structures from the command line. Pick your stack, pass a few flags, and start coding — or define your project in a `.projectme` manifest file.

---

## Quick Start

### Installation

```bash
pip install projectme
```

### Scaffolding

```bash
projectme create my-app react
projectme create my-app nextjs --tailwind
projectme create my-server express --rest --ts
projectme create my-api python --fastapi
```

Or build from a manifest file:

```bash
projectme read manifest
```

For full usage, options, and examples, see [DOCUMENTATION.md](DOCUMENTATION.md).

---

## Feedback

We welcome feedback and suggestions to help improve the project. Thank you!

---

## License

[MIT](LICENSE)