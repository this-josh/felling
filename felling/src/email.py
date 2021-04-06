from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import List, Optional, Sequence, Tuple, Union
import ssl
import os
import re
import logging

logger = logging.getLogger(__name__)


def check_email_address(email_to_check: str):
    """
    Check an email address is valid

    Parameters
    ----------
    email_to_check : str
        Email address to check

    Raises
    ------
    ValueError
        If the email address is not RFC_5322 compliant
    """
    RFC_5322_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    match = re.match(RFC_5322_regex, email_to_check)
    if match is None:
        raise ValueError(f"{email_to_check} is not a valid email address")


def _get_sender_and_password(
    sender: Optional[str], password: Optional[str]
) -> Tuple[str, str]:
    """
    Get the sender email address and password

    Parameters
    ----------
    sender : Optional[str]
        Sender email address provided
    password : Optional[str]
        Sender email password provided

    Returns
    -------
    Tuple[str, str]
        The sender email address and password

    Raises
    ------
    ValueError
        If the sender email address cannot be determined
    ValueError
        If the sender password cannot be determined
    """
    if sender is None:
        sender = os.getenv("felling_email_sender")
        if sender is None:
            raise ValueError(
                f"No sender email was provided to send_email and the environment variable is {sender}"
            )
        logger.info(f"Got {sender} from environment variable felling_email_sender")

    check_email_address(sender)

    if password is None:
        password = os.getenv("felling_email_password")
        if password is None:
            raise ValueError(
                f"No sender password was provided to send_email and the environment variable is None"
            )

    return sender, password


def send_email(
    to: Union[List[str], str],
    sender: Optional[str] = None,
    password: Optional[str] = None,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    smtp_server: str = "Smtp.office365.com",
):
    """
    A method to easily send emails

    If the email fails to send the error is logged be and error isn't raised

    sender : Optional[str], optional
        [description], by default None
    password : Optional[str], optional
        [description], by default None

    Parameters
    ----------
    to : Union[List[str], str]
        The recipients as a list of strings or an individual string
    sender : Optional[str], optional
        The senders email address if None will look for the environment variable felling_email_sender, by default None
    password : Optional[str], optional
        The senders password, it is reccomended this is stored as an environment variable if None will look for the environment variable felling_email_password, by default None
    subject : Optional[str], optional
        The email subject, if none will try to infer from content, by default None
    content : Optional[str], optional
        The email content, if none will try to infer from subject. Html code can be provided, e.g. from pandas `to_html`, by default None
    smtp_server : str, optional
        The smtp_server to use, currently only tested on office365, by default "Smtp.office365.com"

    Raises
    ------
    TypeError
        If the smtp server is of incorrect type raise this error
    """

    if isinstance(to, str):
        to = [to]

    if subject is None and content is not None:
        subject = content[:30]
    elif subject is not None and content is None:
        content = subject
    elif subject is None and content is None:
        subject = "No subject or content provided."
        content = subject

    if not isinstance(smtp_server, str):
        raise TypeError(f"smtp_server must be a str, not type {type(smtp_server)}")

    message = MIMEMultipart("alt")
    # message.set_content(content)
    message["Subject"] = subject
    message["From"] = sender

    content = MIMEText(content, "html")
    message.attach(content)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port=25) as smtp:
            smtp.starttls(context=context)
            smtp.login(message["From"], password)
            for recipient in to:
                message["To"] = recipient
                smtp.sendmail(message["From"], recipient, message.as_string())
    except Exception as e:
        logger.exception(e)
