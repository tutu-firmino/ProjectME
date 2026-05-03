from enum import Enum
from typing import Annotated

import typer
from projectme.core.scaffold import scaffold

cli = typer.Typer()

class Stack(str, Enum):
    react = "react"
    python = "python"

STACK_OPTIONS = {
    Stack.react: {"--tailwind", "--cra"},
    Stack.python: {"--flask", "--django", "--fastapi", "--no-venv"},
}

def _validate_options(stack: Stack, options: list[str]):
    blocked_options = [
        option for option in options
        if option in STACK_OPTIONS[Stack.react] | STACK_OPTIONS[Stack.python]
        and option not in STACK_OPTIONS[stack]
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
    no_git: Annotated[bool, typer.Option("--no-git")] = False,
    no_venv: Annotated[bool, typer.Option("--no-venv")] = False,
):
    arguments = [f"--{arg}" for arg, val in {
        "tailwind": tailwind, "cra": cra,
        "flask": flask, "django": django, "fastapi": fastapi
    }.items() if val]
    flags = [f"--{flag}" for flag, val in {
        "no-git": no_git, "no-venv": no_venv
    }.items() if val]

    _validate_options(stack, arguments + flags)

    project_path = scaffold(stack=stack.value, name=name, arguments=arguments, flags=flags)
    _print_success(name=name, stack=stack, project_path=project_path, git_enabled=not no_git)

if __name__ == "__main__":
    cli()
