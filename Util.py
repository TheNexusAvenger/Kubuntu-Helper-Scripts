"""
TheNexusAvenger

Common utilities used with the scripts.
"""

import math
import sys
from typing import Dict, List, Optional


def promptConfirm(message: str) -> bool:
    """ Prompts confirming a message. Defaults to "no" (False).

    :param message: Message to prompt.
    :return: Whether the prompt was confirmed.
    """

    result = input(message + " (y/N): ").strip().lower()
    return result == "y" or result == "yes"


def outputOptions(options: List[Dict]) -> None:
    """Outputs a list of options.

    :param: options Option to install.
    """

    leadingZerosFormat = "{:0" + str(math.ceil(math.log(len(options), 10))) + "d}"
    for i in range(0, len(options)):
        installOption = options[i]
        print(leadingZerosFormat.format(i + 1) + ". " + installOption["shortName"] + " - " + installOption["name"])
        print("\t" + installOption["description"])


def getOptions(options: List[Dict], arguments: Optional[List] = None) -> List[int]:
    """Gets the options to select.

    :param: options Options to select from.
    :param: arguments Optional overrides for the command line.
    :return: Set of index options to install.
    """

    # Get or prompt for the arguments.
    if arguments is None:
        arguments = sys.argv[1:]
    if len(arguments) == 0:
        # Prompt for the options.
        print("No install options given. Please specify what to install. Options:")
        outputOptions(options)
        selectedOptions = input()

        # Parse the selected options.
        arguments = selectedOptions.split(" ")

    # Parse the number options.
    for i in range(0, len(arguments)):
        argument = arguments[i].lower()
        if argument.isdigit() and 1 <= int(argument) <= len(options):
            argument = options[int(argument) - 1]["shortName"]
        arguments[i] = argument

    # Determine the unique valid and unique invalid arguments.
    validArguments = []
    invalidArguments = []
    for i in range(0, len(arguments)):
        argument = arguments[i]

        # Get the index of the argument.
        argumentIndex = None
        for j in range(0, len(options)):
            if options[j]["shortName"].lower() == argument:
                argumentIndex = j
                break

        # Add the argument.
        if argumentIndex is not None and argumentIndex not in validArguments:
            validArguments.append(argumentIndex)
        elif argumentIndex is None and argument not in invalidArguments:
            invalidArguments.append(argument)

    # Stop if there are invalid arguments.
    if len(invalidArguments) > 0:
        print("The following are unknown options: " + ", ".join(invalidArguments))
        exit(-1)

    # Return the index of the options.
    return validArguments