import json

from apps.cli.main import main


def test_demo_terminal(capsys):
    assert main(["demo", "--no-color"]) == 0
    out = capsys.readouterr().out
    assert "DEMO" in out
    for rule_id in ("S3-001", "EC2-001", "IAM-001", "CT-001"):
        assert rule_id in out


def test_demo_json(capsys):
    assert main(["demo", "--format", "json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["summary"]["total_findings"] == len(data["findings"]) > 0
    assert data["summary"]["by_severity"]["CRITICAL"] >= 1
