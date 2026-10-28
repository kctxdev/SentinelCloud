from sentinelcloud.rules.s3 import encryption, logging, public_access


def test_s3_rules(load_fixture):
    buckets = load_fixture("s3_buckets.json")
    for module in (public_access, encryption, logging):
        findings = module.check(buckets)
        assert [f.resource for f in findings] == ["bucket-inseguro"]
