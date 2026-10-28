import json

from sentinelcloud.core.scanner import Scanner
from sentinelcloud.reports.csv_report import render_csv
from sentinelcloud.reports.json_report import render_json
from sentinelcloud.reports.terminal_report import render_terminal
from sentinelcloud.security.redaction import redact


def _result(load_fixture):
    return Scanner().scan({"s3": load_fixture("s3_buckets.json")}, account_id="123", region="us-east-1")


def test_json(load_fixture):
    data = json.loads(render_json(_result(load_fixture)))
    assert data["summary"]["total_findings"] == len(data["findings"]) == 3


def test_csv_and_terminal(load_fixture):
    r = _result(load_fixture)
    assert render_csv(r).splitlines()[0].startswith("rule_id")
    assert "S3-001" in render_terminal(r, color=False)


def test_redaction():
    assert "AKIAABCDEFGHIJKLMNOP" not in redact("key AKIAABCDEFGHIJKLMNOP")
    assert "hunter2" not in redact("password=hunter2")
