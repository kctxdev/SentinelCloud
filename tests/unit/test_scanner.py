from sentinelcloud.core.scanner import Scanner


def test_scanner_orders_by_severity(load_fixture):
    data = {
        "s3": load_fixture("s3_buckets.json"),
        "ec2": load_fixture("security_groups.json"),
        "iam": load_fixture("iam_policies.json"),
        "cloudtrail": [],
    }
    result = Scanner().scan(data)
    severities = [int(f.severity) for f in result.findings]
    assert severities == sorted(severities, reverse=True)
    assert result.findings[0].severity.name == "CRITICAL"


def test_scanner_filters_services(load_fixture):
    data = {"s3": load_fixture("s3_buckets.json"), "ec2": load_fixture("security_groups.json")}
    result = Scanner().scan(data, services=["s3"])
    assert {f.service for f in result.findings} == {"s3"}
