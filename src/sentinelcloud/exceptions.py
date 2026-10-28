"""Excecoes do SentinelCloud."""


class SentinelError(Exception):
    """Erro base."""


class AuthenticationError(SentinelError):
    """Falha ao autenticar na AWS."""


class CollectionError(SentinelError):
    """Falha ao coletar dados de um servico."""


class ConfigError(SentinelError):
    """Configuracao invalida."""
