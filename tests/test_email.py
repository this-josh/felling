from email import message
import pytest


@pytest.mark.parametrize(
    "to,sender,password,subject,content",
    (
        ["willow@yew.com", "ash@birch.com", "TreesRCool", None, None],
        [
            ["willow@yew.com", "elm@yew.com"],
            "ash@birch.com",
            "TreesRCool",
            None,
            None,
        ],
        ["willow@yew.com", ["ash@birch.com"], "TreesRCool", None, None],
        [
            "willow@yew.com",
            "ash@birch.com",
            "TreesRCool",
            None,
            "content is important",
        ],
        [
            "willow@yew.com",
            "ash@birch.com",
            "TreesRCool",
            "subjects are useful",
            None,
        ],
        [
            "willow@yew.com",
            "ash@birch.com",
            "TreesRCool",
            "subjects are useful",
            "content is important",
        ],
    ),
    ids=[
        "str sender, one recipient, no subject or content",
        "str sender, two recipients as list, no subject or content",
        "one list sender, one recipient, no subject or content",
        "str sender, one recipient, no subject, has content",
        "str sender, one recipient, has subject no content",
        "str sender, one recipient, has subject and content",
    ],
)
def test_send_email(to, sender, password, subject, content):
    from felling.email import send_email

    send_email(to, sender, password, subject, content, smtp_server="localhost")


def test_office_connections():
    from felling.email import send_email

    send_email(
        "willow@yew.com",
        "ash@birch.com",
        "TreesRCool",
        None,
        None,
    )


def test_send_email_invalid():
    from felling.email import send_email

    with pytest.raises(
        ValueError,
        match=r"More than one sender has been provided, only sender address should be provided as a string. sender = \['ash@birch.com', 'pine@birch.com']",
    ):
        send_email(
            "willow@yew.com",
            ["ash@birch.com", "pine@birch.com"],
            "TreesRCool",
            "subjects are useful",
            "content is important",
            smtp_server="localhost",
        )


def test_send_email_smtp_server():
    from felling.email import send_email

    with pytest.raises(
        TypeError, match="smtp_server must be a str, not type <class 'int'>"
    ):
        send_email(
            "willow@yew.com",
            "ash@birch.com",
            "TreesRCool",
            None,
            None,
            smtp_server=35930,
        )


def test_send_email_mock_smtp(mocker):
    from felling.email import send_email, smtplib
    from smtplib import SMTP

    class mock_smtp(SMTP):
        def __init__(self, server, port=None) -> None:
            self.server = server
            self.port = port

        def starttls(self, context):
            return None

        def login(self, email, passwd):
            return None

        def sendmail(self, sender, recipient, message):
            return None

    mocker.patch("smtplib.SMTP", mock_smtp)

    send_email(
        "willow@yew.com",
        "ash@birch.com",
        "TreesRCool",
        None,
        None,
    )


@pytest.mark.parametrize(
    "address_to_check", (("YEW"), ("not an email"), ("ash@birch."))
)
def test_check_email_address_invalid(address_to_check):
    from felling.email import check_email_address

    with pytest.raises(
        ValueError, match=address_to_check + " is not a valid email address"
    ):
        check_email_address(address_to_check)


@pytest.mark.parametrize(
    "address_to_check", (("ash@birch-yew.co"), ("beach@pine.co.uk"), ("ash@birch.com"))
)
def test_check_email_address_valid(address_to_check):
    from felling.email import check_email_address

    check_email_address(address_to_check)


def test_get_sender_and_password_valid_env():
    from felling.email import _get_sender_and_password
    import os

    os.environ.clear()

    os.environ["felling_email_sender"] = "willow@yew.com"
    os.environ["felling_email_password"] = "TreesRCool"

    _get_sender_and_password(None, None)


def test_get_sender_and_password_invalid_email():
    from felling.email import _get_sender_and_password
    import os

    os.environ.clear()

    os.environ["felling_email_password"] = "TreesRCool"
    with pytest.raises(
        ValueError,
        match="No sender email was provided to send_email and the environment variable is None",
    ):
        _get_sender_and_password(None, None)


def test_get_sender_and_password_invalid_password():
    from felling.email import _get_sender_and_password
    import os

    os.environ.clear()

    os.environ["felling_email_sender"] = "willow@yew.com"
    with pytest.raises(
        ValueError,
        match="No sender password was provided to send_email and the environment variable is None",
    ):
        _get_sender_and_password(None, None)
