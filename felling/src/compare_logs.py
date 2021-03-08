import logging
from typing import List
import re
import argparse

# configure()
logger = logging.getLogger(__name__)


def parse_args(cli_arguments):

    parser = argparse.ArgumentParser(description="Compare two log files")
    parser.add_argument(
        "first_file",
        metavar="first_file",
        type=str,
        nargs=1,
        help="first log file",
    )
    parser.add_argument(
        "second_file",
        metavar="second_file",
        type=str,
        nargs=1,
        help="second log file",
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="How verbose to work"
    )

    args = parser.parse_args(cli_arguments)
    return args.first_file[0], args.second_file[0], args.verbose


def read_file(file_name: str) -> List[str]:
    """
    Read in a text file

    Parameters
    ----------
    file_name : str
        The text file path as a str to read

    Returns
    -------
    List[str]
        The text files content
    """
    with open(file_name, "r") as f:
        return f.readlines()


def tidy_logs(logs: List[str]) -> List[str]:
    """
    Extract log messages from logs

    Remove intiail logs, times, file name, etc.

    Parameters
    ----------
    logs : List[str]
        The logs

    Returns
    -------
    List[str]
        Only the log messages
    """

    log_messages = []
    for log in logs:
        log = log.strip()
        # Ensure log message starts with a 4 digit number to check it is a new log message
        if re.match(r"^[0-9]{4}", log):
            # Could I split using the format in logger.json?
            log_message = re.split(r"- on line [0-9]* - ", log)[1]
            log_message = log_message.rsplit(" - ", 1)[0]
            log_messages.append(log_message)
        else:
            # We must be mid-message!
            log_messages.append(log)
    return log_messages


def find_differences(
    f1_log_messages: List[str], f2_log_messages: List[str], verbose: int
):
    """
    If a difference exists, write where they exist

    This method may not be the fastest, have tested on two 20k line log files and it is <1 second

    Parameters
    ----------
    f1_log_messages : List[str]
        The first files log messages
    f2_log_messages : List[str]
        The second files log messages
    verbose : int
        Whether to work verbose
    """

    num_differences = 0
    max_differences = 100 if verbose == 0 else None
    to_print = True
    print(
        f"Note provided log number provided will likely be slightly (~15) lines smaller than the actual line number"
    )
    if len(f1_log_messages) != len(f2_log_messages):
        print(
            f"First file has len {len(f1_log_messages)}, second has len {len(f2_log_messages)}, will print differences until the first file is exhausted."
        )
        max_lines = min((len(f1_log_messages), len(f2_log_messages)))
    else:
        max_lines = len(f1_log_messages)

    for log_number in range(max_lines):
        if f1_log_messages[log_number] != f2_log_messages[log_number]:
            num_differences += 1
            if to_print:
                # \U00002757 prints a nice red ! Oh no!
                print(
                    f"\U00002757 Log number {log_number} is not identical for both files. \nfile_1[log_number] = {f1_log_messages[log_number]} \nfile_2[log_number] = {f2_log_messages[log_number]}"
                )
        if max_differences is not None and num_differences >= max_differences:
            if to_print:
                print(
                    f"{num_differences} differences have been printed, the maximum without verbose. Pass -v to get all differences"
                )
            to_print = False

    print(f"{num_differences} differences exist")


def compare_log_file(file_1: str, file_2: str, verbose: int):
    """
    Compare two log files

    Parameters
    ----------
    file_1 : str
        The first log file to read
    file_2 : str
        The second log file to read
    verbose : int
        Whether to work verbosely
    """
    f1_logs = read_file(file_1)
    f2_logs = read_file(file_2)

    f1_log_messages = tidy_logs(f1_logs)
    f2_log_messages = tidy_logs(f2_logs)

    if f1_log_messages == f2_log_messages:
        # \U0001F600 prints a smiley emoji :)
        print(
            "\U0001F600\U0001F600\U0001F600Woo! the logs messages are identical\U0001F600\U0001F600\U0001F600"
        )
    else:
        find_differences(f1_log_messages, f2_log_messages, verbose)
