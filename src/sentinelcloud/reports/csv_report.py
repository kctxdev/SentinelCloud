"""Relatorio CSV."""
import csv
import io

from ..core.scanner import ScanResult

COLUMNS = ["rule_id", "severity", "service", "resource", "title", "description", "remediation"]


def render_csv(result: ScanResult) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for f in result.findings:
        writer.writerow(f.to_dict())
    return buf.getvalue()
