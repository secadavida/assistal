import smtplib
from email.message import EmailMessage
import mimetypes
import assistal.settings as S

def send_email(subject: str, body: str, to_email: str, from_email: str, password: str, attachment_path: str = None):
    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Add attachment if provided
    if attachment_path:
        mime_type, _ = mimetypes.guess_type(attachment_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        mime_main, mime_sub = mime_type.split('/', 1)

        with open(attachment_path, 'rb') as file:
            msg.add_attachment(file.read(), maintype=mime_main, subtype=mime_sub, filename=attachment_path)

    # Get SMTP settings based on the domain of the from_email
    _, domain = from_email.split('@', 1)
    smtp_settings = S.SMTP_SETTINGS.get(domain)
    if not smtp_settings:
        return False

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(smtp_settings[0], smtp_settings[1]) as server:
            server.login(from_email, password)
            server.send_message(msg)
    except Exception:
        return False

    return True
