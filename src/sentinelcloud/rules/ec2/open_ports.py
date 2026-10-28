"""EC2-001: portas sensiveis abertas para a internet."""
from ...core.finding import Finding
from ...core.severity import Severity
from ..registry import rule

SENSITIVE = {22: "SSH", 3389: "RDP", 3306: "MySQL", 5432: "PostgreSQL",
             1433: "MSSQL", 6379: "Redis", 27017: "MongoDB", 9200: "Elasticsearch"}
OPEN_CIDRS = ("0.0.0.0/0", "::/0")


def _open_to_world(perm: dict) -> bool:
    v4 = any(r.get("CidrIp") in OPEN_CIDRS for r in perm.get("IpRanges", []))
    v6 = any(r.get("CidrIpv6") in OPEN_CIDRS for r in perm.get("Ipv6Ranges", []))
    return v4 or v6


@rule("EC2-001", "ec2", "Security Group com portas sensiveis abertas ao mundo")
def check(groups: list) -> list[Finding]:
    out = []
    for g in groups:
        gid = g.get("GroupId", "?")
        for perm in g.get("IpPermissions", []):
            if not _open_to_world(perm):
                continue
            proto = perm.get("IpProtocol")
            if proto == "-1":
                out.append(Finding(
                    rule_id="EC2-001", service="ec2", severity=Severity.CRITICAL, resource=gid,
                    title="Todo o trafego liberado para a internet",
                    description="Regra de entrada com protocolo -1 aberta para 0.0.0.0/0 ou ::/0.",
                    remediation="Restrinja a origem e as portas ao minimo necessario.",
                ))
                continue
            lo, hi = perm.get("FromPort"), perm.get("ToPort")
            if lo is None or hi is None:
                continue
            for port, name in SENSITIVE.items():
                if lo <= port <= hi:
                    out.append(Finding(
                        rule_id="EC2-001", service="ec2", severity=Severity.HIGH, resource=gid,
                        title=f"Porta {port} ({name}) aberta para a internet",
                        description=f"Security group {gid} permite {name} de qualquer origem.",
                        remediation="Limite a origem a IPs conhecidos, VPN ou bastion/SSM.",
                    ))
    return out
