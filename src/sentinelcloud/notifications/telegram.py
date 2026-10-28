"""Notificacao via Telegram."""
import json
import urllib.request

from ..config import Settings


def send_telegram(settings: Settings, text: str) -> None:
    if not (settings.telegram_token and settings.telegram_chat_id):
        raise ValueError("Telegram nao configurado (SENTINEL_TELEGRAM_TOKEN / CHAT_ID).")
    url = f"https://api.telegram.org/bot{settings.telegram_token}/sendMessage"
    body = json.dumps({"chat_id": settings.telegram_chat_id, "text": text[:4000]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15):
        pass
