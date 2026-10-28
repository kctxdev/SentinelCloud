"""Relatorio JSON."""
import json

from ..core.scanner import ScanResult
from .summary import build_summary


def render_json(result: ScanResult) -> str:
    payload = {"summary": build_summary(result), "findings": [f.to_dict() for f in result.findings]}
    return json.dumps(payload, indent=2, ensure_ascii=False)
