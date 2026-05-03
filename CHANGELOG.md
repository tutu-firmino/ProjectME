# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-05-03

### Added

- `projectme read manifest` command to build projects from a `.projectme` manifest file
- `.projectme` TOML manifest format with `[project]`, `[args]`, `[flags]`, and `[meta]` sections
- Manifest validation (required keys, type checking, unknown section/key detection, stack validation)
- Next.js stack with App Router, Pages Router, `--src`, `--tailwind`, `--eslint`, `--turbopack`, and `--js` options
- Express stack with `--rest`, `--env`, `--ts`, and `--docker` options
- `--src` option for Next.js (src directory layout)
- `--pages-router` option for Next.js
- `--eslint` option for Next.js
- `--turbopack` option for Next.js
- `--js` option for Next.js (JavaScript instead of TypeScript)
- `--rest` option for Express (REST boilerplate)
- `--env` option for Express (`.env.example`)
- `--ts` option for Express (TypeScript)
- `--docker` option for Express (Dockerfile + `.dockerignore`)
- Tests for the manifest feature (`test_manifest.py`)

## [0.3.0] 2025-05-02

### Added

- Initial release
- React (Vite) and Python scaffolding
- Git initialization by default
- `--cra` flag for React (Create React App scaffolding)
- `--fastapi` flag for Python (FastAPI scaffolding)
- Stack-specific option validation
- `--flask` and `--django` flags for Python
- `--no-venv` flag for Python
- `--tailwind` flag for React
- `--no-git` flag for all stacks