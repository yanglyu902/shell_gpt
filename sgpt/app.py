"""
shell-gpt: An interface to OpenAI's ChatGPT (GPT-3.5) API

This module provides a simple interface for OpenAI's ChatGPT API using Typer
as the command line interface. It supports different modes of output including
shell commands and code, and allows users to specify the desired OpenAI model
and length and other options of the output. Additionally, it supports executing
shell commands directly from the interface.

API Key is stored locally for easy use in future runs.
"""


import os

import typer

# Click is part of typer.
from click import MissingParameter
from sgpt import config, make_prompt, OpenAIClient
from sgpt.utils import (
    loading_spinner,
    typer_writer,
)


@loading_spinner
def get_completion(
    prompt: str,
    temperature: float,
    top_p: float,
    caching: bool,
):
    api_host = config.get("OPENAI_API_HOST")
    api_key = config.get("OPENAI_API_KEY")
    client = OpenAIClient(api_host, api_key)
    return client.get_completion(
        message=prompt,
        model="gpt-3.5-turbo",
        temperature=temperature,
        top_probability=top_p,
        caching=caching,
    )


def main(
    prompt: str = typer.Argument(None, show_default=False, help="The prompt to generate completions for."),
    temperature: float = typer.Option(0.7, min=0.0, max=1.0, help="Randomness of generated output."),
    top_probability: float = typer.Option(1.0, min=0.1, max=1.0, help="Limits highest probable tokens (words)."),
    shell: bool = typer.Option(False, "--shell", "-s", help="Provide shell command as output."),
    cache: bool = typer.Option(True, help="Cache completion results."),
) -> None:

    if not prompt:
        raise MissingParameter(param_hint="PROMPT", param_type="string")

    if shell:
        temperature = 0.4
        prompt = make_prompt.shell(prompt)
    
    completion = get_completion(
        prompt, temperature, top_probability, cache
    )

    typer_writer(completion, shell)
    
    if shell and typer.confirm("Execute shell command?"):
        os.system(completion)


def entry_point() -> None:
    # Python package entry point defined in setup.py
    typer.run(main)


if __name__ == "__main__":
    entry_point()
