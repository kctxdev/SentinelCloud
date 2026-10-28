"""SentinelCloud - scanner de seguranca para ambientes AWS.

Coleta configuracoes de S3, Security Groups, IAM e CloudTrail, aplica regras
de seguranca (somente leitura) e gera relatorios com pontuacao de risco.
"""
from .config import Settings
from .exceptions import (
    AuthenticationError,
    CollectionError,
    ConfigError,
    SentinelError,
)

__version__ = "0.1.0"
__author__ = "kactxn.dev"

__all__ = [
    "__version__",
    "__author__",
    "Settings",
    "SentinelError",
    "AuthenticationError",
    "CollectionError",
    "ConfigError",
]