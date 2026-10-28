"""S3-003: logs de acesso."""
from ...core.finding import Finding
from ...core.severity import Severity
from ..registry import rule


@rule("S3-003", "s3", "Bucket sem logs de acesso")
def check(buckets: list) -> list[Finding]:
    return [
        Finding(
            rule_id="S3-003", service="s3", severity=Severity.LOW, resource=b["name"],
            title="Bucket sem logs de acesso",
            description="Server access logging esta desativado.",
            remediation="Habilite server access logging para um bucket de logs dedicado.",
        )
        for b in buckets if not b.get("logging")
    ]
