"""Calculo de pontuacao de risco."""
from __future__ import annotations

from collections import Counter
from typing import Iterable

from .finding import Finding


def risk_score(findings: Iterable[Finding]) -> int:
    """Soma ponderada limitada a 100."""
    total = sum(f.severity.weight for f in findings)
    return min(total, 100)


def risk_rating(score: int) -> str:
    if score == 0:
        return "NONE"
    if score < 10:
        return "LOW"
    if score < 30:
        return "MEDIUM"
    if score < 60:
        return "HIGH"
    return "CRITICAL"


def count_by_severity(findings: Iterable[Finding]) -> dict[str, int]:
    counter = Counter(f.severity.name for f in findings)
    return {name: counter.get(name, 0) for name in ("CRITICAL", "HIGH", "MEDIUM", "LOW")}
