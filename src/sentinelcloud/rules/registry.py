"""Registro de regras via decorator."""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Callable

from ..core.finding import Finding

RuleFunc = Callable[[list], list[Finding]]


@dataclass(frozen=True)
class Rule:
    id: str
    service: str
    title: str
    func: RuleFunc


_RULES: dict[str, Rule] = {}

_MODULES = [
    "sentinelcloud.rules.s3.public_access",
    "sentinelcloud.rules.s3.encryption",
    "sentinelcloud.rules.s3.logging",
    "sentinelcloud.rules.ec2.open_ports",
    "sentinelcloud.rules.iam.excessive_permissions",
    "sentinelcloud.rules.cloudtrail.audit_logging",
]


def rule(rule_id: str, service: str, title: str):
    def decorator(func: RuleFunc) -> RuleFunc:
        _RULES[rule_id] = Rule(rule_id, service, title, func)
        return func
    return decorator


def load_rules() -> list[Rule]:
    for module in _MODULES:
        importlib.import_module(module)
    return sorted(_RULES.values(), key=lambda r: r.id)
