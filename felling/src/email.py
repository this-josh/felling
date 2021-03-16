from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import List, Optional, Union
import ssl
import logging

logger = logging.getLogger(__name__)


def send_email(
    sender: str,
    password: str,
    to: Union[List[str], str],
    subject: Optional[str] = None,
    content: Optional[str] = None,
    smtp_server: str = "Smtp.office365.com",
):
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

    context = ssl.SSLContext()
    try:
        with smtplib.SMTP(smtp_server, port=25) as smtp:
            smtp.starttls(context=context)
            smtp.login(message["From"], password)
            for recipient in to:
                message["To"] = recipient
                smtp.sendmail(message["From"], recipient, message.as_string())
    except Exception as e:
        logger.exception(e)
