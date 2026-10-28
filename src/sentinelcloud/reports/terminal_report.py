"""Relatorio para terminal."""
from ..core.scanner import ScanResult
from .summary import build_summary

COLORS = {"CRITICAL": "\033[95m", "HIGH": "\033[91m", "MEDIUM": "\033[93m", "LOW": "\033[94m"}
RESET = "\033[0m"


def render_terminal(result: ScanResult, color: bool = True) -> str:
    s = build_summary(result)
    lines = [
        "=" * 60,
        f"SentinelCloud - conta {s['account_id']} ({s['region']})",
        "=" * 60,
        f"Achados: {s['total_findings']} | Risco: {s['risk_score']}/100 ({s['risk_rating']})",
        "  " + "  ".join(f"{k}: {v}" for k, v in s["by_severity"].items()),
        "",
    ]
    for f in result.findings:
        tag = f"[{f.severity.name}]"
        if color:
            tag = f"{COLORS[f.severity.name]}{tag}{RESET}"
        lines.append(f"{tag} {f.rule_id} {f.resource} - {f.title}")
        lines.append(f"    {f.description}")
        if f.remediation:
            lines.append(f"    Correcao: {f.remediation}")
    if not result.findings and not result.errors:
        lines.append("Nenhum achado. Bom trabalho!")
    if result.errors:
        lines.append("")
        lines.append("ATENCAO: nao foi possivel verificar (provavel falta de permissao):")
        for service, message in result.errors.items():
            lines.append(f"  - {service}: {message}")
        lines.append("  Estes servicos NAO foram analisados; o resultado esta incompleto.")
    return "\n".join(lines)
