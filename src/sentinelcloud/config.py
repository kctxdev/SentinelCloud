"""Configuracao carregada de variaveis de ambiente."""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    profile: str | None = None
    region: str = "us-east-1"
    telegram_token: str | None = None
    telegram_chat_id: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = field(default=None, repr=False)
    email_from: str | None = None
    email_to: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        env = os.environ
        return cls(
            profile=env.get("AWS_PROFILE"),
            region=env.get("AWS_REGION", "us-east-1"),
            telegram_token=env.get("SENTINEL_TELEGRAM_TOKEN"),
            telegram_chat_id=env.get("SENTINEL_TELEGRAM_CHAT_ID"),
            smtp_host=env.get("SENTINEL_SMTP_HOST"),
            smtp_port=int(env.get("SENTINEL_SMTP_PORT", "587")),
            smtp_user=env.get("SENTINEL_SMTP_USER"),
            smtp_password=env.get("SENTINEL_SMTP_PASSWORD"),
            email_from=env.get("SENTINEL_EMAIL_FROM"),
            email_to=env.get("SENTINEL_EMAIL_TO"),
        )
