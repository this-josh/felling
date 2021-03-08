import pytest

with open("./tests/sample_logs/19700101-0000_create_sample_logs.log", "r") as f:
    sample_logs_1 = f.readlines()

with open("./tests/sample_logs/19700101-0001_create_sample_logs.log", "r") as f:
    sample_logs_2 = f.readlines()

simple_sample_logs = [
    "1970-01-01 00:00:00 - __main__ - INFO - create_sample_logs.<module> - on line 6 - Ash - /Users/Ash",
    "1970-01-01 00:00:00 - __main__ - INFO - create_sample_logs.<module> - on line 9 - 5 has randomly been chosen. - /Users/Ash",
    "1970-01-01 00:00:00 - __main__ - INFO - create_sample_logs.<module> - on line 11 - 5 squared is 25 - /Users/Ash",
    "1970-01-01 00:00:00 - __main__ - INFO - create_sample_logs.<module> - on line 13 - 5 + 10 is 15 - /Users/Ash",
]


@pytest.mark.parametrize(
    "cli_args,expected",
    [
        (["Ash", "Birch"], ["Ash", "Birch", 0]),
        (["Ash", "Birch", "-v"], ["Ash", "Birch", 1]),
    ],
    ids=["Two files, less verbose", "Two files, more verbose"],
)
def test_parse_args(cli_args, expected):
    from felling.src.compare_logs import parse_args

    first_file, second_file, verbose = parse_args(cli_args)

    assert first_file == expected[0]
    assert second_file == expected[1]
    assert verbose == expected[2]


# TODO: Need a test for felling.src.compare_logs.read_file


def test_tidy_logs():
    from felling.src.compare_logs import tidy_logs

    expected_logs = [
        "Ash",
        "5 has randomly been chosen.",
        "5 squared is 25",
        "5 + 10 is 15",
    ]
    tidied_logs = tidy_logs(simple_sample_logs)
    assert tidied_logs == expected_logs


# TODO: Need a test for felling.src.compare_logs.find_differences


@pytest.mark.parametrize(
    ("logs_1", "logs_2", "verbosity"),
    [
        (sample_logs_1, sample_logs_1, 0),
        (sample_logs_1, sample_logs_1, 1),
        (sample_logs_1, sample_logs_2, 0),
        (sample_logs_1, sample_logs_2, 1),
        (sample_logs_1, sample_logs_2[:-40], 0),
        (sample_logs_1, sample_logs_2[:-40], 1),
    ],
    ids=[
        "Identical logs, less verbose",
        "Identical logs, more verbose",
        "Different logs, less verbose",
        "Different logs, more verbose",
        "Different length logs, less verbose",
        "Different length logs, more verbose",
    ],
)
def test_find_difference(logs_1, logs_2, verbosity):
    from felling.src.compare_logs import find_differences

    find_differences(logs_1, logs_2, verbosity)


@pytest.mark.parametrize(
    ("first_file", "second_file", "verbosity"),
    [
        (
            "./tests/sample_logs/19700101-0000_create_sample_logs.log",
            "./tests/sample_logs/19700101-0000_create_sample_logs.log",
            0,
        ),
        (
            "./tests/sample_logs/19700101-0000_create_sample_logs.log",
            "./tests/sample_logs/19700101-0000_create_sample_logs.log",
            1,
        ),
        (
            "./tests/sample_logs/19700101-0000_create_sample_logs.log",
            "./tests/sample_logs/19700101-0001_create_sample_logs.log",
            0,
        ),
        (
            "./tests/sample_logs/19700101-0000_create_sample_logs.log",
            "./tests/sample_logs/19700101-0001_create_sample_logs.log",
            1,
        ),
    ],
)
def test_compare_log_file(first_file, second_file, verbosity):
    """Test compare log file, this is only a rough test that nothing fails"""
    from felling.src.compare_logs import compare_log_file

    # identical files
    compare_log_file(first_file, second_file, verbosity)
