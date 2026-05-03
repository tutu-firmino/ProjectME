from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from projectme.core.manifest import read_and_build
from projectme.core.scaffold import scaffold

cli = typer.Typer()


class Stack(str, Enum):
    react = "react"
    python = "python"
    nextjs = "nextjs"
    express = "express"


STACK_OPTIONS = {
    Stack.react: {"--tailwind", "--cra"},
    Stack.python: {"--flask", "--django", "--fastapi", "--no-venv"},
    Stack.nextjs: {"--tailwind", "--src", "--pages-router", "--eslint", "--js", "--turbopack"},
    Stack.express: {"--rest", "--env", "--ts", "--docker"},
}

ALL_STACK_OPTIONS = set().union(*STACK_OPTIONS.values())


def _validate_options(stack: Stack, options: list[str]):
    blocked_options = [
        option
        for option in options
        if option in ALL_STACK_OPTIONS and option not in STACK_OPTIONS[stack]
    ]

    if blocked_options:
        option_list = ", ".join(blocked_options)
        raise typer.BadParameter(f"{option_list} cannot be used with the {stack.value} stack")


def _print_success(name: str, stack: Stack, project_path, git_enabled: bool):
    typer.secho("Project created", fg=typer.colors.GREEN, bold=True)

    typer.echo("  Name:  ", nl=False)
    typer.secho(name, fg=typer.colors.CYAN)

    typer.echo("  Stack: ", nl=False)
    typer.secho(stack.value, fg=typer.colors.CYAN)

    typer.echo("  Path:  ", nl=False)
    typer.secho(str(project_path), fg=typer.colors.CYAN)

    typer.echo("  Git:   ", nl=False)
    if git_enabled:
        typer.secho("initialized", fg=typer.colors.GREEN)
    else:
        typer.secho("skipped", fg=typer.colors.YELLOW)


@cli.callback()
def main():
    pass


@cli.command()
def create(
    name: str,
    stack: Stack,
    tailwind: Annotated[bool, typer.Option("--tailwind")] = False,
    cra: Annotated[bool, typer.Option("--cra")] = False,
    flask: Annotated[bool, typer.Option("--flask")] = False,
    django: Annotated[bool, typer.Option("--django")] = False,
    fastapi: Annotated[bool, typer.Option("--fastapi")] = False,
    src: Annotated[bool, typer.Option("--src")] = False,
    pages_router: Annotated[bool, typer.Option("--pages-router")] = False,
    eslint: Annotated[bool, typer.Option("--eslint")] = False,
    js: Annotated[bool, typer.Option("--js")] = False,
    turbopack: Annotated[bool, typer.Option("--turbopack")] = False,
    rest: Annotated[bool, typer.Option("--rest")] = False,
    env: Annotated[bool, typer.Option("--env")] = False,
    ts: Annotated[bool, typer.Option("--ts")] = False,
    docker: Annotated[bool, typer.Option("--docker")] = False,
    no_git: Annotated[bool, typer.Option("--no-git")] = False,
    no_venv: Annotated[bool, typer.Option("--no-venv")] = False,
):
    arguments = [
        f"--{arg}"
        for arg, val in {
            "tailwind": tailwind,
            "cra": cra,
            "flask": flask,
            "django": django,
            "fastapi": fastapi,
            "src": src,
            "pages-router": pages_router,
            "eslint": eslint,
            "rest": rest,
            "env": env,
        }.items()
        if val
    ]
    flags = [
        f"--{flag}"
        for flag, val in {
            "no-git": no_git,
            "no-venv": no_venv,
            "js": js,
            "turbopack": turbopack,
            "ts": ts,
            "docker": docker,
        }.items()
        if val
    ]

    _validate_options(stack, arguments + flags)

    project_path = scaffold(stack=stack.value, name=name, arguments=arguments, flags=flags)
    _print_success(name=name, stack=stack, project_path=project_path, git_enabled=not no_git)


read_app = typer.Typer()
cli.add_typer(read_app, name="read")


@read_app.command()
def manifest(
    path: Annotated[
        Path | None,
        typer.Option("--path", help="Directory containing the .projectme manifest file"),
    ] = None,
):
    result = read_and_build(path)

    typer.secho("Manifest read and project built!", fg=typer.colors.GREEN, bold=True)

    typer.echo("  Name:  ", nl=False)
    typer.secho(result["name"], fg=typer.colors.CYAN)

    typer.echo("  Stack: ", nl=False)
    typer.secho(result["stack"], fg=typer.colors.CYAN)

    typer.echo("  Path:  ", nl=False)
    typer.secho(result["where"], fg=typer.colors.CYAN)

    typer.echo("  Args:  ", nl=False)
    typer.secho(
        ", ".join(a.lstrip("-") for a in result["args"]) or "none",
        fg=typer.colors.CYAN,
    )

    typer.echo("  Flags: ", nl=False)
    typer.secho(
        ", ".join(f.lstrip("-") for f in result["flags"]) or "none",
        fg=typer.colors.CYAN,
    )

if __name__ == "__main__":
    cli()
