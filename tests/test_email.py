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
    from felling.src.email import send_email

    send_email(to, sender, password, subject, content, smtp_server="localhost")

    from felling.src.email import send_email

    send_email(sender, password, to, subject, content, smtp_server="localhost")


def test_send_email_smtp_server():
    from felling.src.email import send_email

    with pytest.raises(
        TypeError, match="smtp_server must be a str, not type <class 'int'>"
    ):
        send_email(
            "ash@birch.com",
            "TreesRCool",
            "willow@yew.com",
            None,
            None,
            smtp_server=35930,
        )
