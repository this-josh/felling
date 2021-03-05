import sys
from felling.src.compare_logs import compare_log_file, parse_args


if __name__ == "__main__":
    first_file, second_file, verbose = parse_args(sys.argv[1:])
    compare_log_file(first_file, second_file, verbose)
