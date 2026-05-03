import subprocess
from pathlib import Path

import pytest

from projectme.core.scaffold import scaffold
from projectme.stacks import python, react


def test_react_files_stay_in_project(tmp_path):
    project_path = scaffold(
        stack="react",
        name="web",
        arguments=["--tailwind"],
        flags=["--no-git"],
        path=tmp_path,
    )

    assert project_path == tmp_path / "web"
    assert project_path.joinpath("src", "App.jsx").is_file()
    assert project_path.joinpath("public", "vite.svg").is_file()
    assert project_path.joinpath("tailwind.config.js").is_file()
    assert not tmp_path.joinpath("src", "App.jsx").exists()
    assert not tmp_path.joinpath("package.json").exists()


def test_python_files_stay_in_project(tmp_path):
    project_path = scaffold(
        stack="python",
        name="service",
        arguments=["--fastapi"],
        flags=["--no-git", "--no-venv"],
        path=tmp_path,
    )

    assert project_path == tmp_path / "service"
    assert project_path.joinpath("src", "main.py").is_file()
    assert project_path.joinpath("src", "routes.py").is_file()
    assert project_path.joinpath("requirements.txt").is_file()
    assert not tmp_path.joinpath("src", "main.py").exists()
    assert not tmp_path.joinpath("requirements.txt").exists()


def test_default_path_is_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    project_path = scaffold(
        stack="python",
        name="local",
        arguments=[],
        flags=["--no-git", "--no-venv"],
    )

    assert project_path == tmp_path / "local"
    assert project_path.joinpath("src", "main.py").is_file()


@pytest.mark.parametrize("stack", ["react", "python"])
def test_invalid_project_names_fail(stack, tmp_path):
    with pytest.raises(ValueError, match="invalid character"):
        scaffold(
            stack=stack,
            name="bad name",
            arguments=[],
            flags=["--no-git", "--no-venv"],
            path=tmp_path,
        )


def test_unknown_stack_fails(tmp_path):
    with pytest.raises(ValueError, match="invalid value for 'stack'"):
        scaffold(stack="rails", name="app", arguments=[], flags=[], path=tmp_path)


def test_stack_and_name_are_required():
    with pytest.raises(TypeError, match="missing 2 required arguments"):
        scaffold(stack=None, name=None, arguments=[], flags=[])

    with pytest.raises(TypeError, match="missing required argument: 'stack'"):
        scaffold(stack=None, name="app", arguments=[], flags=[])

    with pytest.raises(TypeError, match="missing required argument: 'name'"):
        scaffold(stack="python", name=None, arguments=[], flags=[])


def test_react_git_runs_quietly_in_project(tmp_path, monkeypatch):
    calls = []

    def fake_run(args, cwd=None, stdout=None, stderr=None):
        calls.append((args, Path(cwd), stdout, stderr))
        return subprocess.CompletedProcess(args=args, returncode=0)

    monkeypatch.setattr(react.subprocess, "run", fake_run)

    project_path = react.build("web", tmp_path, arguments=[], flags=[])

    assert project_path == tmp_path / "web"
    assert calls == [
        (["git", "init"], project_path, subprocess.DEVNULL, subprocess.DEVNULL),
    ]


def test_python_tools_run_in_project(tmp_path, monkeypatch):
    calls = []

    def fake_run(args, cwd=None, stdout=None, stderr=None):
        calls.append((args, Path(cwd), stdout, stderr))
        return subprocess.CompletedProcess(args=args, returncode=0)

    monkeypatch.setattr(python.subprocess, "run", fake_run)

    project_path = python.build("service", tmp_path, arguments=[], flags=[])

    assert project_path == tmp_path / "service"
    assert calls == [
        (["git", "init"], project_path, subprocess.DEVNULL, subprocess.DEVNULL),
        (["python", "-m", "venv", ".venv"], project_path, None, None),
    ]
