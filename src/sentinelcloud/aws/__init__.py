"""Integracao com a AWS: sessao, autenticacao, conta e coletores.

O boto3 so e importado quando uma sessao e criada, entao este pacote pode
ser importado sem o boto3 instalado (util nos testes).
"""
from .account import get_account_id
from .authentication import caller_identity
from .permissions import REQUIRED_ACTIONS, policy_document
from .session import create_session

__all__ = [
    "create_session",
    "caller_identity",
    "get_account_id",
    "REQUIRED_ACTIONS",
    "policy_document",
]
