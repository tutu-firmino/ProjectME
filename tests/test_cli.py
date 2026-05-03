import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from projectme.main import cli
from projectme.stacks import python, react

runner = CliRunner()


def _fake_git_init(args, cwd=None, stdout=None, stderr=None):
    assert args == ["git", "init"]
    assert stdout is subprocess.DEVNULL
    assert stderr is subprocess.DEVNULL
    Path(cwd, ".git").mkdir()
    return subprocess.CompletedProcess(args=args, returncode=0)


def test_react_app_created(monkeypatch):
    monkeypatch.setattr(react.subprocess, "run", _fake_git_init)

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["create", "my-app", "react", "--tailwind"])

        assert result.exit_code == 0
        assert "Initialized empty Git repository" not in result.output
        assert "Project created" in result.output
        assert "Name:  my-app" in result.output
        assert "Stack: react" in result.output
        assert "Path:  " in result.output
        assert "Git:   initialized" in result.output

        project = Path("my-app")
        assert project.joinpath(".git").is_dir()
        assert project.joinpath("src", "App.jsx").is_file()
        assert project.joinpath("tailwind.config.js").is_file()
        assert not Path("src", "App.jsx").exists()


def test_python_app_without_git_or_venv():
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["create", "api", "python", "--no-git", "--no-venv"])

        assert result.exit_code == 0
        assert "Project created" in result.output
        assert "Stack: python" in result.output
        assert "Git:   skipped" in result.output

        project = Path("api")
        assert project.joinpath("src", "main.py").is_file()
        assert not project.joinpath(".git").exists()
        assert not project.joinpath(".venv").exists()
        assert not Path("src", "main.py").exists()


def test_python_app_sets_up_tools_in_project(monkeypatch):
    calls = []

    def fake_run(args, cwd=None, stdout=None, stderr=None):
        calls.append((args, Path(cwd), stdout, stderr))
        if args == ["git", "init"]:
            assert stdout is subprocess.DEVNULL
            assert stderr is subprocess.DEVNULL
            Path(cwd, ".git").mkdir()
        elif args == ["python", "-m", "venv", ".venv"]:
            Path(cwd, ".venv").mkdir()
        else:
            pytest.fail(f"unexpected subprocess call: {args}")
        return subprocess.CompletedProcess(args=args, returncode=0)

    monkeypatch.setattr(python.subprocess, "run", fake_run)

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["create", "service", "python"])

        assert result.exit_code == 0
        assert "Git:   initialized" in result.output
        assert calls == [
            (["git", "init"], Path("service").resolve(), subprocess.DEVNULL, subprocess.DEVNULL),
            (["python", "-m", "venv", ".venv"], Path("service").resolve(), None, None),
        ]
        assert Path("service", ".git").is_dir()
        assert Path("service", ".venv").is_dir()


@pytest.mark.parametrize(
    ("args", "blocked_option"),
    [
        (["create", "bad", "python", "--tailwind", "--no-git", "--no-venv"], "--tailwind"),
        (["create", "bad", "python", "--cra", "--no-git", "--no-venv"], "--cra"),
        (["create", "bad", "react", "--flask", "--no-git"], "--flask"),
        (["create", "bad", "react", "--django", "--no-git"], "--django"),
        (["create", "bad", "react", "--fastapi", "--no-git"], "--fastapi"),
        (["create", "bad", "react", "--no-venv", "--no-git"], "--no-venv"),
    ],
)
def test_wrong_stack_options_fail(args, blocked_option):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, args)

        assert result.exit_code != 0
        assert f"{blocked_option} cannot be used" in result.output
        assert not Path("bad").exists()


def test_unknown_stack_fails():
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["create", "bad", "rails"])

        assert result.exit_code != 0
        assert "Invalid value" in result.output
        assert "react" in result.output
        assert "python" in result.output
        assert not Path("bad").exists()
