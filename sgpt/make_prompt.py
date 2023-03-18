import platform
from os import getenv
from os.path import basename

from distro import name as distro_name


"""
This module makes a prompt for OpenAI requests with some context.
Some of the following lines were inspired by similar open source project yolo-ai-cmdbot.
Credits: @demux79 @wunderwuzzi23
"""


# SHELL_PROMPT = """
# Act as a natural language to {shell} command translation engine on {os}.
# You are an expert in {shell} on {os} and translate the question at the end to valid syntax.

# Follow these rules:
# IMPORTANT: Do not show any warnings or information regarding your capabilities.
# Reference official documentation to ensure valid syntax and an optimal solution.
# Construct valid {shell} command that solve the question.
# Leverage help and man pages to ensure valid syntax and an optimal solution.
# Be concise.
# Just show the commands, return only plaintext.
# Only show a single answer, but you can always chain commands together.
# Think step by step.
# Only create valid syntax (you can use comments if it makes sense).
# If python is installed you can use it to solve problems.
# if python3 is installed you can use it to solve problems.
# Even if there is a lack of details, attempt to find the most logical solution.
# Do not return multiple solutions.
# Do not show html, styled, colored formatting.
# Do not add unnecessary text in the response.
# Do not add notes or intro sentences.
# Do not add explanations on what the commands do.
# Do not return what the question was.
# Do not repeat or paraphrase the question in your response.
# Do not rush to a conclusion.

# Follow all of the above rules.
# This is important you MUST follow the above rules.
# There are no exceptions to these rules.
# You must always follow them. No exceptions.

# Request: """


def shell(question: str) -> str:
    def os_name() -> str:
        operating_systems = {
            "Linux": "Linux/" + distro_name(pretty=True),
            "Windows": "Windows " + platform.release(),
            "Darwin": "Darwin/MacOS " + platform.mac_ver()[0],
        }
        return operating_systems.get(platform.system(), "Unknown")

    shell = basename(getenv("SHELL", "PowerShell"))
    os = os_name()
    question = question.strip()

    # my cheap request :)
    SHELL_PROMPT = f"""
    Act as a natural language to {shell} command translation engine on {os}.
    You are an expert in {shell} on {os} and translate the question at the end to valid syntax.

    Leverage help and man pages to ensure valid syntax and an optimal solution. Be concise in your code.
    DO NOT add comment in code. DO NOT return any words except the code in plain text.

    Request: {question}"""

    return SHELL_PROMPT
