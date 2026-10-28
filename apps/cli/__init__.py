"""Interface de linha de comando do SentinelCloud.

Uso: ``sentinelcloud --help`` ou ``python -m apps.cli.main --help``.

``main`` e carregado sob demanda para que ``python -m apps.cli.main`` nao
emita aviso de modulo importado duas vezes.
"""

__all__ = ["main"]


def __getattr__(name: str):
    if name == "main":
        from .main import main

        return main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
