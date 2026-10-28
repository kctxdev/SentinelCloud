"""S3-001: bloqueio de acesso publico."""
from ...core.finding import Finding
from ...core.severity import Severity
from ..registry import rule

FLAGS = ("BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets")


@rule("S3-001", "s3", "Bucket sem bloqueio completo de acesso publico")
def check(buckets: list) -> list[Finding]:
    out = []
    for b in buckets:
        pab = b.get("public_access_block")
        missing = list(FLAGS) if not pab else [f for f in FLAGS if not pab.get(f)]
        if missing:
            out.append(Finding(
                rule_id="S3-001", service="s3", severity=Severity.HIGH, resource=b["name"],
                title="Bucket sem bloqueio completo de acesso publico",
                description=f"Configuracoes ausentes/desativadas: {', '.join(missing)}.",
                remediation="Ative as 4 opcoes de S3 Block Public Access no bucket e na conta.",
            ))
    return out
