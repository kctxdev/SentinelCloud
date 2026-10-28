"""Despacha notificacoes pelos canais escolhidos."""
from ..config import Settings
from ..core.scanner import ScanResult
from ..reports.summary import build_summary
from .email import send_email
from .telegram import send_telegram


def _message(result: ScanResult) -> str:
    s = build_summary(result)
    return (
        f"SentinelCloud - conta {s['account_id']}\n"
        f"Achados: {s['total_findings']} | Risco: {s['risk_score']}/100 ({s['risk_rating']})\n"
        + ", ".join(f"{k}={v}" for k, v in s["by_severity"].items())
    )


def dispatch(settings: Settings, result: ScanResult, channels: list[str]) -> None:
    text = _message(result)
    for ch in channels:
        if ch == "telegram":
            send_telegram(settings, text)
        elif ch == "email":
            send_email(settings, "SentinelCloud - resultado do scan", text)
        else:
            raise ValueError(f"Canal desconhecido: {ch}")
