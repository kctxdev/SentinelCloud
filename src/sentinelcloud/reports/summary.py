"""Resumo textual do scan."""
from ..core.scanner import ScanResult


def build_summary(result: ScanResult) -> dict:
    return {
        "account_id": result.account_id,
        "region": result.region,
        "total_findings": len(result.findings),
        "by_severity": result.counts,
        "risk_score": result.score,
        "risk_rating": result.rating,
        "collection_errors": dict(result.errors),
    }
