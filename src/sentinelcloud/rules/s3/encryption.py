"""S3-002: criptografia em repouso."""
from ...core.finding import Finding
from ...core.severity import Severity
from ..registry import rule


@rule("S3-002", "s3", "Bucket sem criptografia padrao")
def check(buckets: list) -> list[Finding]:
    return [
        Finding(
            rule_id="S3-002", service="s3", severity=Severity.MEDIUM, resource=b["name"],
            title="Bucket sem criptografia padrao",
            description="Nenhuma configuracao de criptografia padrao encontrada.",
            remediation="Habilite SSE-S3 (AES256) ou SSE-KMS como padrao.",
        )
        for b in buckets if not b.get("encryption")
    ]
