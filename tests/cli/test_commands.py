from apps.cli.main import main


def test_version(capsys):
    assert main(["version"]) == 0
    assert "sentinelcloud" in capsys.readouterr().out


def test_rules(capsys):
    assert main(["rules"]) == 0
    out = capsys.readouterr().out
    for rule_id in ("S3-001", "EC2-001", "IAM-001", "CT-001"):
        assert rule_id in out
