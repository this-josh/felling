import pytest

sample_logs = [
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
    tidied_logs = tidy_logs(sample_logs)
    assert tidied_logs == expected_logs


# TODO: Need a test for felling.src.compare_logs.find_differences


def test_compare_log_file():
    """Test compare log file, this is only a rough test that nothing fails"""
    from felling.src.compare_logs import compare_log_file

    compare_log_file(
        "./tests/sample_logs/19700101-0000_create_sample_logs.log",
        "./tests/sample_logs/19700101-0000_create_sample_logs.log",
        0,
    )

    compare_log_file(
        "./tests/sample_logs/19700101-0000_create_sample_logs.log",
        "./tests/sample_logs/19700101-0000_create_sample_logs.log",
        1,
    )
