"""Notificacoes do resultado do scan: Telegram e e-mail."""
from .dispatcher import dispatch
from .email import send_email
from .telegram import send_telegram

__all__ = ["dispatch", "send_telegram", "send_email"]
