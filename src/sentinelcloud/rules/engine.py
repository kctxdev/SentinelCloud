"""Executa regras registradas."""
from __future__ import annotations

from ..core.finding import Finding
from .registry import load_rules


class RuleEngine:
    def run(self, data: dict[str, list], services: list[str] | None = None) -> list[Finding]:
        findings: list[Finding] = []
        for r in load_rules():
            if services and r.service not in services:
                continue
            if r.service not in data:
                continue
            findings.extend(r.func(data[r.service]))
        return findings
