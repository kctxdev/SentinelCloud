"""Modelo de achado de seguranca."""
from __future__ import annotations

from dataclasses import dataclass

from .severity import Severity


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: Severity
    resource: str
    description: str
    remediation: str = ""
    service: str = ""

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "severity": self.severity.name,
            "service": self.service,
            "resource": self.resource,
            "description": self.description,
            "remediation": self.remediation,
        }
