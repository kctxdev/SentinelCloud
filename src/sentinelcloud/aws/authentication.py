"""Validacao de credenciais."""
from __future__ import annotations

from ..exceptions import AuthenticationError


def caller_identity(session) -> dict:
    try:
        return session.client("sts").get_caller_identity()
    except Exception as exc:
        raise AuthenticationError(f"Credenciais invalidas ou ausentes: {exc}") from exc
