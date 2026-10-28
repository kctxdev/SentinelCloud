"""CT-001: CloudTrail ativo."""
from ...core.finding import Finding
from ...core.severity import Severity
from ..registry import rule


@rule("CT-001", "cloudtrail", "CloudTrail ausente ou desativado")
def check(trails: list) -> list[Finding]:
    if not trails:
        return [Finding(
            rule_id="CT-001", service="cloudtrail", severity=Severity.HIGH, resource="account",
            title="Nenhuma trilha do CloudTrail configurada",
            description="A conta nao possui trilhas; atividades de API nao sao registradas.",
            remediation="Crie uma trilha multi-regiao com validacao de integridade de logs.",
        )]
    out = []
    for t in trails:
        if not t.get("is_logging"):
            out.append(Finding(
                rule_id="CT-001", service="cloudtrail", severity=Severity.HIGH, resource=t["name"],
                title="Trilha do CloudTrail desativada",
                description="A trilha existe, mas o registro de eventos esta parado.",
                remediation="Reative o logging da trilha.",
            ))
    if trails and not any(t.get("multi_region") for t in trails):
        out.append(Finding(
            rule_id="CT-001", service="cloudtrail", severity=Severity.MEDIUM, resource="account",
            title="Nenhuma trilha multi-regiao",
            description="Eventos de outras regioes podem nao ser registrados.",
            remediation="Habilite IsMultiRegionTrail em pelo menos uma trilha.",
        ))
    return out
