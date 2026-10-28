"""Scanner: aplica regras sobre dados ja coletados."""
from __future__ import annotations

from dataclasses import dataclass, field

from ..rules.engine import RuleEngine
from .finding import Finding
from .risk_engine import count_by_severity, risk_rating, risk_score


@dataclass
class ScanResult:
    findings: list[Finding] = field(default_factory=list)
    account_id: str = "unknown"
    region: str = ""
    # servicos que nao puderam ser coletados: {"iam": "mensagem de erro"}
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def score(self) -> int:
        return risk_score(self.findings)

    @property
    def rating(self) -> str:
        return risk_rating(self.score)

    @property
    def counts(self) -> dict[str, int]:
        return count_by_severity(self.findings)


class Scanner:
    def __init__(self, engine: RuleEngine | None = None):
        self.engine = engine or RuleEngine()

    def scan(self, data: dict[str, list], services: list[str] | None = None,
             account_id: str = "unknown", region: str = "",
             errors: dict[str, str] | None = None) -> ScanResult:
        findings = self.engine.run(data, services)
        findings.sort(key=lambda f: (-int(f.severity), f.service, f.resource))
        return ScanResult(findings=findings, account_id=account_id, region=region,
                          errors=dict(errors or {}))
