"""Notificacao via e-mail (SMTP com STARTTLS)."""
import smtplib
from email.message import EmailMessage

from ..config import Settings


def send_email(settings: Settings, subject: str, body: str) -> None:
    if not (settings.smtp_host and settings.email_from and settings.email_to):
        raise ValueError("E-mail nao configurado (SENTINEL_SMTP_HOST / EMAIL_FROM / EMAIL_TO).")
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, settings.email_from, settings.email_to
    msg.set_content(body)
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as smtp:
        smtp.starttls()
        if settings.smtp_user:
            smtp.login(settings.smtp_user, settings.smtp_password or "")
        smtp.send_message(msg)
