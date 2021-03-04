import argparse
from difflib import get_close_matches
from felling.compare_logs import compare_log_file


def parse_args():
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
    parser.add_argument("-v", "--verbose", action="count", default=0)

    args = parser.parse_args()
    print(args)
    return args.first_file[0], args.second_file[0], args.verbose


if __name__ == "__main__":
    first_file, second_file, verbose = parse_args()
    compare_log_file(first_file, second_file, verbose)