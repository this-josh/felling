import logging
from felling import configure
import sys

# configure()
logger = logging.getLogger(__name__)


def read_file(f):
    with open(f, "r") as f:
        return f.readlines()


def tidy_logs(logs):
    import re

    log_messages = []
    for log in logs:
        # Could I split using the format in logger.json?
        log_message = re.split(r"- on line [0-9]* - ", log)[1]
        log_message = log_message.rsplit(" - ", 1)[0]
        log_messages.append(log_message)
    return log_messages


def find_differences(f1_log_messages, f2_log_messages, verbose):
    num_differences = 0
    max_differences = 100 if verbose == 1 else None
    to_print = True
    for log_number in range(len(f1_log_messages)):
        if f1_log_messages[log_number] != f2_log_messages[log_number]:
            if num_differences == 0:
                print(
                    f"Note provided log number provided will likely be slightly (<15) lines smaller than the actual line number"
                )
            num_differences += 1
            if to_print:
                print(
                    f"Log number {log_number} is not identical between both files. \nfile_1[log_number] = {f1_log_messages[log_number]} \nfile_2[log_number] = {f2_log_messages[log_number]}"
                )
        if max_differences is not None and num_differences >= max_differences:
            if to_print:
                print(
                    f"{num_differences} have been printed, the maximum without verbose. Pass -v to get all differences"
                )
            to_print = False

    print(f"{num_differences} differences exist")


def compare_log_file(file_1, file_2, verbose):

    f1_logs = read_file(file_1)
    f2_logs = read_file(file_2)

    f1_log_messages = tidy_logs(f1_logs)
    f2_log_messages = tidy_logs(f2_logs)

    if f1_log_messages == f2_log_messages:
        print("Woo! the logs messages are identical")
    else:
        find_differences(f1_log_messages, f2_log_messages, verbose)


# compare_log_file("sample_logs/210304-1200_run.log", "sample_logs/different.log")
