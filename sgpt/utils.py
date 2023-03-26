import os
from time import sleep
from typing import Callable
from tempfile import NamedTemporaryFile

import typer

from click import BadParameter
from rich.progress import Progress, SpinnerColumn, TextColumn
from sgpt import OpenAIClient


def loading_spinner(func: Callable) -> Callable:
    """
    Decorator that adds a loading spinner animation to a function that uses the OpenAI API.

    :param func: Function to wrap.
    :return: Wrapped function with loading.
    """
    def wrapper(*args, **kwargs):
        text = TextColumn("[green]Consulting with robots...")
        with Progress(SpinnerColumn(), text, transient=True) as progress:
            progress.add_task("request")
            return func(*args, **kwargs)
    return wrapper


def typer_writer(text: str, shell: bool) -> None:
    """
    Writes output to the console, with optional typewriter animation and color.

    :param text: Text to output.
    :param code: If content of text is code.
    :param shell: if content of text is shell command.
    :param animate: Enable/Disable typewriter animation.
    :return: None
    """
    color = "yellow" if shell else None
    if not shell:
        for char in text:
            typer.secho(char, nl=False, fg=color, bold=shell)
            sleep(0.01)
        # Add new line at the end, to prevent % from appearing.
        typer.echo("")
        return
    typer.secho(text, fg=color, bold=shell)
