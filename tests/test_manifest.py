import pytest

from projectme.core.manifest import _search_manifest, _validate_manifest, read_and_build

# ---------------------------------------------------------------------------
# _search_manifest
# ---------------------------------------------------------------------------


def test_search_manifest_raises_when_no_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError, match="no .projectme file found"):
        _search_manifest()


def test_search_manifest_reads_toml(tmp_path, monkeypatch):
    manifest = tmp_path / ".projectme"
    manifest.write_text(
        '[project]\nname = "my-app"\nstack = "react"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    data = _search_manifest()
    assert data == {"project": {"name": "my-app", "stack": "react"}}


# ---------------------------------------------------------------------------
# _validate_manifest — valid cases
# ---------------------------------------------------------------------------


def test_validate_minimal_valid():
    _validate_manifest({"project": {"name": "app", "stack": "react"}})


def test_validate_full_manifest():
    _validate_manifest(
        {
            "project": {"name": "app", "stack": "python", "where": "/projects/app"},
            "args": {
                "flask": True,
                "django": False,
                "fastapi": False,
                "tailwind": False,
                "cra": False,
                "eslint": False,
                "pages-router": False,
                "src": False,
                "rest": False,
                "env": False,
            },
            "flags": {
                "no-git": True,
                "no-venv": False,
                "turbopack": False,
                "js": False,
                "ts": False,
                "docker": False,
            },
            "meta": {"author": "me", "version": "1.0", "description": "test"},
        }
    )


# ---------------------------------------------------------------------------
# _validate_manifest — errors
# ---------------------------------------------------------------------------


def test_validate_missing_project_section():
    with pytest.raises(ValueError, match="missing required section '\\[project\\]'"):
        _validate_manifest({"args": {"tailwind": True}})


def test_validate_missing_required_key():
    with pytest.raises(ValueError, match="missing required key 'name'"):
        _validate_manifest({"project": {"stack": "react"}})


def test_validate_unknown_section():
    with pytest.raises(ValueError, match="unknown section"):
        _validate_manifest({"project": {"name": "a", "stack": "react"}, "unknown": {}})


def test_validate_unknown_key():
    with pytest.raises(ValueError, match="unknown key 'bad-key'"):
        _validate_manifest({"project": {"name": "a", "stack": "react", "bad-key": "x"}})


def test_validate_wrong_type():
    with pytest.raises(ValueError, match="expected str, got int"):
        _validate_manifest({"project": {"name": 123, "stack": "react"}})


def test_validate_wrong_type_for_bool_arg():
    with pytest.raises(ValueError, match="expected bool, got str"):
        _validate_manifest(
            {"project": {"name": "a", "stack": "react"}, "args": {"tailwind": "yes"}}
        )


def test_validate_unknown_stack():
    with pytest.raises(ValueError, match="unknown stack 'rails'"):
        _validate_manifest({"project": {"name": "a", "stack": "rails"}})


# ---------------------------------------------------------------------------
# read_and_build — integration
# ---------------------------------------------------------------------------


def test_read_and_build_react(tmp_path, monkeypatch):
    manifest = tmp_path / ".projectme"
    manifest.write_text(
        '[project]\nname = "web"\nstack = "react"\n'
        "[args]\ntailwind = true\n"
        "[flags]\nno-git = true\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    read_and_build()

    project = tmp_path / "web"
    assert project.joinpath("src", "App.jsx").is_file()
    assert project.joinpath("tailwind.config.js").is_file()
    assert not project.joinpath(".git").exists()


def test_read_and_build_python(tmp_path, monkeypatch):
    manifest = tmp_path / ".projectme"
    manifest.write_text(
        '[project]\nname = "api"\nstack = "python"\n'
        "[args]\nfastapi = true\n"
        "[flags]\nno-git = true\nno-venv = true\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    read_and_build()

    project = tmp_path / "api"
    assert project.joinpath("src", "main.py").is_file()
    assert project.joinpath("src", "routes.py").is_file()
    assert project.joinpath("requirements.txt").is_file()
    assert not project.joinpath(".git").exists()
    assert not project.joinpath(".venv").exists()


def test_read_and_build_with_where(tmp_path, monkeypatch):
    target = tmp_path / "output"
    target.mkdir()

    where_str = str(target).replace("\\", "/")

    manifest = tmp_path / ".projectme"
    manifest.write_text(
        f'[project]\nname = "app"\nstack = "python"\nwhere = "{where_str}"\n'
        "[flags]\nno-git = true\nno-venv = true\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    read_and_build()

    project = target / "app"
    assert project.joinpath("src", "main.py").is_file()


def test_read_and_build_no_manifest(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError, match="no .projectme file found"):
        read_and_build()


def test_read_and_build_invalid_manifest(tmp_path, monkeypatch):
    manifest = tmp_path / ".projectme"
    manifest.write_text(
        '[project]\nname = "app"\nstack = "unknown"\n',
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError, match="unknown stack"):
        read_and_build()


def test_read_and_build_express(tmp_path, monkeypatch):
    manifest = tmp_path / ".projectme"
    manifest.write_text(
        '[project]\nname = "server"\nstack = "express"\n'
        "[args]\nrest = true\n"
        "[flags]\nno-git = true\nts = true\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    read_and_build()

    project = tmp_path / "server"
    assert project.joinpath("src", "index.ts").is_file()
    assert project.joinpath("src", "routes", "index.ts").is_file()
    assert project.joinpath("tsconfig.json").is_file()


def test_read_and_build_nextjs(tmp_path, monkeypatch):
    manifest = tmp_path / ".projectme"
    manifest.write_text(
        '[project]\nname = "frontend"\nstack = "nextjs"\n'
        "[args]\ntailwind = true\nsrc = true\n"
        "[flags]\nno-git = true\njs = true\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    read_and_build()

    project = tmp_path / "frontend"
    assert project.joinpath("src", "app", "page.jsx").is_file()
    assert project.joinpath("tailwind.config.js").is_file()
