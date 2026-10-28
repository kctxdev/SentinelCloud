"""Informacoes da conta."""
from __future__ import annotations

from .authentication import caller_identity


def get_account_id(session) -> str:
    return caller_identity(session)["Account"]
