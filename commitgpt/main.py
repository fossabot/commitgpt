import typer
from rich import print
from .gitop import Git
from .gpt import GPT
import configparser
from .prompts import (
    TIM_COMMIT_GUIDELINE,
    ROLE,
)
from rich.progress import Progress, SpinnerColumn, TextColumn

from typing_extensions import Annotated
from typing import Optional
import os
from pathlib import Path

APP_NAME = "commitgpt"

APP_DIR = typer.get_app_dir(APP_NAME)

CONFIG_PATH: Path = Path(APP_DIR) / "config.cfg"


__version__ = "0.2.0"

app = typer.Typer(
    name=APP_NAME,
    help="Generate a commit message based on the provided Git diff.",
)

git = Git()

gpt = GPT()


def get_config(path: str = CONFIG_PATH) -> (str, str, str):
    """get_config
    If the config file exists, read the config file.
    If the config file does not exist, prompt the user for the config values
    and create the config file.

    Args:
        path (str, optional): config path. Defaults to CONFIG_PATH.

    Returns:
        (str, str, str): openai api key, commit guidelines, role
    """

    config = configparser.RawConfigParser()

    if not path.is_file():
        print("[bold red]Config file not found![/bold red] :scream:\n[bold green]Setting up commitgpt...[/bold green] :tada:")  # noqa: E501

        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
        if OPENAI_API_KEY == "":
            OPENAI_API_KEY = typer.prompt(
                "OpenAI API key from https://platform.openai.com/account/api-keys",
                default=os.environ.get("OPENAI_API_KEY", ""),
                hide_input=True,
                confirmation_prompt=True,
                type=str,
            )

        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        config.add_section(APP_NAME)
        config.set(APP_NAME, 'openai_api_key', OPENAI_API_KEY)
        config.set(APP_NAME, 'commit_guidelines', TIM_COMMIT_GUIDELINE)
        config.set(APP_NAME, 'role', ROLE)
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
        print("[bold green]Config file created![/bold green] :tada:")

    config.read(path)

    return config.get(APP_NAME, 'openai_api_key'), config.get(APP_NAME, 'commit_guidelines'), config.get(APP_NAME, 'role')  # noqa: E501


@app.callback(invoke_without_command=True)
def callback(
    after_add: bool = typer.Option(False, "--after-add", "-a"),
    signoff: bool = typer.Option(False, "--signoff", "-s"),
    config: Annotated[
        Optional[Path], typer.Option(
            mode="r",
            show_default=False,
            help="Config file path"
        )
    ] = None
):
    """Generate a commit message based on the provided Git diff.
    """
    if config is None:
        config = CONFIG_PATH

    api_key, commit_guidelines, professional_role = get_config(config)

    if api_key != "":
        gpt.api_key(api_key)
    else:
        statement = f"[bold red]OpenAI API key not found. Please set openai_api_key in the config file at {config}! [/bold red] :scream:"  # noqa: E501
        print(statement)
        raise typer.Exit(code=1)

    last_commit_id = git.last_commit_id()
    if last_commit_id == "":
        typer.echo("No commits found.")
        raise typer.Exit(code=0)

    diff = git.diff(commit_id=last_commit_id, after_add=after_add)
    if diff == "":
        typer.echo("No changes to commit.")
        raise typer.Exit(code=0)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Generating...", total=None)
        proposed_commit_message = gpt.generate_message(
            diff, professional_role, commit_guidelines)

    edit = typer.confirm(f"This is the proposed commit message:\n\n{proposed_commit_message}\n\nWould you like to edit it?", default=False)  # noqa: E501
    if edit:
        proposed_commit_message = typer.edit(proposed_commit_message)
        confirm = typer.confirm(f"This is the new proposed commit message:\n\n{proposed_commit_message}\n\nDoes it look good?", default=True)  # noqa: E501
        if confirm:
            git.commit(message=proposed_commit_message, signoff=signoff)
            typer.echo("Commit created!")
        else:
            typer.echo("Commit not created.\nRun `commitgpt` again to generate a new commit message.")  # noqa: E501
    else:
        confirm = typer.confirm("Would you like to create a commit with this message?", default=True)  # noqa: E501
        if confirm:
            git.commit(message=proposed_commit_message, signoff=signoff)
            typer.echo("Commit created!")
        else:
            typer.echo("Commit not created.\nRun `commitgpt` again to generate a new commit message.")  # noqa: E501


@app.command(name="setup")
def setup(
    config: Annotated[
        Optional[Path], typer.Argument(
            case_sensitive=True,
            writable=True,
            mode="r",
            show_default=False,
            help="Config file path"
        )
    ] = CONFIG_PATH
):
    """Setup commitgpt.
    """
    if config is None:
        config = CONFIG_PATH
    _, _, _ = get_config(config)
    typer.echo("Run `commitgpt` to generate a commit message.")
    typer.Exit(code=0)


def version_callback(value: bool):
    if value:
        typer.echo(f"commitgpt version: {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    """
    Generate a commit message based on the provided Git diff.
    """
    if ctx.invoked_subcommand is None:
        callback()
