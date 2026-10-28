"""Nucleo: modelos, scanner, pontuacao de risco e orquestrador.

``Scanner``, ``ScanResult`` e ``Orchestrator`` sao carregados sob demanda
(lazy) para evitar import circular com o pacote ``rules``.
"""
from .severity import Severity
from .finding import Finding
from .risk_engine import count_by_severity, risk_rating, risk_score

_LAZY = {
    "Scanner": ".scanner",
    "ScanResult": ".scanner",
    "Orchestrator": ".orchestrator",
}

__all__ = [
    "Severity",
    "Finding",
    "risk_score",
    "risk_rating",
    "count_by_severity",
    *_LAZY,
]


def __getattr__(name: str):
    if name in _LAZY:
        from importlib import import_module

        module = import_module(_LAZY[name], __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
