import smtplib
from email.message import EmailMessage

import assistal.settings as S

def send_email(subject: str, body: str, to_email: str, from_email: str, password: str):
    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    _, domain = from_email.split('@', 1)
    smtp_settings = S.SMTP_SETTINGS.get(domain)
    if not smtp_settings:
        return False

    try:
        with smtplib.SMTP_SSL(smtp_settings[0], smtp_settings[1]) as server:
            server.login(from_email, password)
            server.send_message(msg)
    except Exception:
        return False

    return True
