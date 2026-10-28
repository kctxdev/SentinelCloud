"""IAM-001: politicas com permissoes excessivas."""
from ...core.finding import Finding
from ...core.severity import Severity
from ..registry import rule


def _as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


@rule("IAM-001", "iam", "Politica IAM com permissoes excessivas")
def check(policies: list) -> list[Finding]:
    out = []
    for pol in policies:
        for stmt in _as_list(pol.get("document", {}).get("Statement")):
            if stmt.get("Effect") != "Allow":
                continue
            actions = _as_list(stmt.get("Action"))
            resources = _as_list(stmt.get("Resource"))
            if "*" in actions and "*" in resources:
                sev, desc = Severity.CRITICAL, "Permite todas as acoes em todos os recursos (acesso administrativo)."
            elif "*" in actions:
                sev, desc = Severity.HIGH, "Permite todas as acoes (Action: *)."
            elif any(a.endswith(":*") for a in actions) and "*" in resources:
                sev, desc = Severity.MEDIUM, "Permite todas as acoes de um servico em todos os recursos."
            else:
                continue
            out.append(Finding(
                rule_id="IAM-001", service="iam", severity=sev, resource=pol.get("name", "?"),
                title="Politica IAM com permissoes excessivas", description=desc,
                remediation="Aplique o principio do menor privilegio: limite acoes e recursos.",
            ))
    return out
