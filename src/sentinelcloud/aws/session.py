"""Criacao de sessao boto3 (somente leitura)."""
from __future__ import annotations

from ..exceptions import AuthenticationError


def list_profiles() -> list[str]:
    """Perfis AWS configurados na maquina (~/.aws). Lista vazia se nao houver."""
    try:
        import boto3

        return sorted(boto3.session.Session().available_profiles)
    except Exception:
        return []


def create_session(
    profile: str | None = None,
    region: str = "us-east-1",
    access_key: str | None = None,
    secret_key: str | None = None,
    session_token: str | None = None,
):
    """Cria a sessao. As chaves, se informadas, ficam apenas na memoria."""
    try:
        import boto3
    except ImportError as exc:  # pragma: no cover
        raise AuthenticationError("boto3 nao instalado. Rode: pip install boto3") from exc
    try:
        if access_key and secret_key:
            return boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                aws_session_token=session_token or None,
                region_name=region,
            )
        return boto3.Session(profile_name=profile, region_name=region)
    except Exception as exc:
        raise AuthenticationError(f"Nao foi possivel criar sessao AWS: {exc}") from exc
