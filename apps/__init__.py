"""Aplicacoes que usam o pacote ``sentinelcloud``.

Hoje existe apenas a interface de linha de comando, em ``apps.cli``.
Para executa-la: ``sentinelcloud --help`` ou ``python -m apps.cli.main --help``.
"""
from . import cli

__all__ = ["cli"]
