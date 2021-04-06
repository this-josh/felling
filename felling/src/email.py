from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import List, Optional, Union
import ssl
import logging

logger = logging.getLogger(__name__)


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
