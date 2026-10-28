from sentinelcloud.rules.ec2.open_ports import check


def test_open_ports(load_fixture):
    findings = check(load_fixture("security_groups.json"))
    by_resource = {f.resource: f.severity.name for f in findings}
    assert by_resource == {"sg-aberto": "HIGH", "sg-tudo": "CRITICAL"}
