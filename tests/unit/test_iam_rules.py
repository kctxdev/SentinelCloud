from sentinelcloud.rules.iam.excessive_permissions import check


def test_excessive_permissions(load_fixture):
    findings = check(load_fixture("iam_policies.json"))
    assert len(findings) == 1
    assert findings[0].resource == "admin"
    assert findings[0].severity.name == "CRITICAL"
