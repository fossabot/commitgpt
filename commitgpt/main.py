from enum import Enum
import click
import typer
from rich import print

from commitgpt.update import check_and_update
from commitgpt.gitop import Git
from commitgpt.gpt import GPT
from commitgpt import __APP_NAME__, __VERSION__
import configparser
from commitgpt.prompts import (
    TIM_COMMIT_GUIDELINE,
    COVENTIONAL_COMMIT_GUIDELINE,
    ROLE,
)
from rich.progress import Progress, SpinnerColumn, TextColumn

from typing_extensions import Annotated
from typing import Optional
import os
from pathlib import Path


class Guidelines(str, Enum):
    tim = "tim"
    conventional = "conventional"



APP_DIR = typer.get_app_dir(__APP_NAME__)
CONFIG_PATH: Path = Path(APP_DIR) / "config.cfg"



app = typer.Typer(
    name=__APP_NAME__,
    help="Generate a commit message based on the provided Git diff.",
)

git = Git()

gpt = GPT(temp_loc=APP_DIR)


def get_config(path: str = CONFIG_PATH) -> (str, str, str, str):
    """get_config
    If the config file exists, read the config file.
    If the config file does not exist, prompt the user for the config values
    and create the config file.

    Args:
        path (str, optional): config path. Defaults to CONFIG_PATH.

    Returns:
        (str, str, str, str): openai api key, commit guidelines, role, signoff
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
        signoff = typer.confirm("Add signoff to commit message?", default=True)
        click_choices = click.Choice(
            ["tim", "conventional"],
            case_sensitive=False,
        )
        guideline = typer.prompt(
            text="Commit guidelines to follow either tim or conventional",
            default="tim",
            show_default=True,
            type=click_choices,
        )
        if guideline == "tim":
            commit_guidelines = TIM_COMMIT_GUIDELINE
        elif guideline == "conventional":
            commit_guidelines = COVENTIONAL_COMMIT_GUIDELINE

        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        config.add_section(__APP_NAME__)
        config.set(__APP_NAME__, 'openai_api_key', OPENAI_API_KEY)
        config.set(__APP_NAME__, 'signoff', signoff)
        config.set(__APP_NAME__, 'commit_guidelines', commit_guidelines)
        config.set(__APP_NAME__, 'role', ROLE)
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
        print("[bold green]Config file created![/bold green] :tada:")

    config.read(path)

    return config.get(__APP_NAME__, 'openai_api_key'), config.get(__APP_NAME__, 'commit_guidelines'), config.get(__APP_NAME__, 'role'), config.getboolean(__APP_NAME__, 'signoff')  # noqa: E501


@ app.callback(invoke_without_command=True)
def callback(
    openai_api_key: Optional[str] = None,
    commit_guideline: Optional[str] = None,
    signoff: Optional[bool] = True,
    config_path: Optional[Path] = None,
):
    """
    `callback` is the main function that is called when the user
    runs `commitgpt`

    Args:
        `openai_api_key` (str, optional): openai api key.
        Defaults to None.

        `commit_guideline` (str, optional): commit guideline.
        Defaults to None.

        `signoff` (bool, optional): add signoff to commit message.
        Defaults to True.

        `config` (Path, optional): config file path.
        Defaults to None.

    Raises:
        `typer.Exit`: exit with code 1 if openai api key is not found.

        `typer.Exit`: exit with code 0 if there are no changes to commit.

    """

    if config_path is None:
        config_path = CONFIG_PATH

    api_key, guideline, role, sign_off = get_config(config_path)
    if openai_api_key is not None:
        api_key = openai_api_key
    if commit_guideline is not None:
        guideline = commit_guideline
    if signoff is not None:
        sign_off = signoff

    if api_key != "":
        gpt.api_key(api_key)
    else:
        print(f"[bold red]OpenAI API key not found. Please set openai_api_key in the config file at {config_path}! [/bold red] :scream:")  # noqa: E501
        raise typer.Exit(code=1)

    diff = git.diff()
    if diff == "":
        typer.echo("No changes to commit.")
        raise typer.Exit(code=0)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Generating commit message...", total=None
        )
        proposed_commit_message = gpt.generate_message(
            git_dif=diff,
            role=role,
            guidelines=guideline
        )

    edit = typer.confirm(f"This is the proposed commit message:\n\n{proposed_commit_message}\n\nWould you like to edit it?", default=False)  # noqa: E501
    if edit:
        proposed_commit_message = typer.edit(proposed_commit_message)
        confirm = typer.confirm(f"This is the new proposed commit message:\n\n{proposed_commit_message}\n\nDoes it look good?", default=True)  # noqa: E501
        if confirm:
            git.commit(message=proposed_commit_message, signoff=sign_off)
            typer.echo("Commit created!")
        else:
            typer.echo("Commit not created.\nRun `commitgpt` again to generate a new commit message.")  # noqa: E501
    else:
        confirm = typer.confirm("Would you like to create a commit with this message?", default=True)  # noqa: E501
        if confirm:
            git.commit(message=proposed_commit_message, signoff=sign_off)
            typer.echo("Commit created!")
        else:
            typer.echo("Commit not created.\nRun `commitgpt` again to generate a new commit message.")  # noqa: E501


@ app.command(name="setup")
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
    """
    Setup commitgpt.
    """
    if config is None:
        config = CONFIG_PATH
    _, _, _, _ = get_config(config)
    typer.echo("Run `commitgpt` to generate a commit message.")
    typer.Exit(code=0)


def version_callback(value: bool = True):
    if value:
        typer.echo(f"commitgpt version: {__VERSION__}")
        raise typer.Exit()


@ app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    openai_api_key: Annotated[
        Optional[str], typer.Option(
            "--openai-api-key",
            "-o",
            envvar="OPENAI_API_KEY",
            show_default=False,
            show_envvar=True,
            help="OpenAI API key from https://platform.openai.com/account/api-keys",
        )
    ] = None,
    commit_guidelines: Annotated[
        Optional[Guidelines], typer.Option(
            "--commit-guidelines",
            "-g",
            show_default=False,
            show_choices=True,
            case_sensitive=False,
            help="Commit guidelines",
        )
    ] = None,
    signoff: bool = typer.Option(
        True,
        "--signoff",
        "-s",
        show_default=True,
        help="Add signoff to commit message.",
    ),
    config_path: Annotated[
        Optional[Path], typer.Option(
            "--config-path",
            "-c",
            mode="r",
            show_default=False,
            help="Config file path. Defaults to {APP_DIR}/config.cfg CLI options take precedence over config file options."  # noqa: E501
        )
    ] = None,
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

    check_and_update()

    if ctx.invoked_subcommand is None:
        callback(
            openai_api_key=openai_api_key,
            commit_guideline=commit_guidelines,
            signoff=signoff,
            config_path=config_path
        )
