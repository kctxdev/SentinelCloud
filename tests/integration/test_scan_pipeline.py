from unittest.mock import patch

from sentinelcloud.core.orchestrator import Orchestrator
from sentinelcloud.config import Settings


def test_pipeline_with_fake_collectors(load_fixture):
    fake = {"s3": lambda s: load_fixture("s3_buckets.json")}
    with patch("sentinelcloud.core.orchestrator.create_session", return_value=object()), \
         patch("sentinelcloud.core.orchestrator.get_account_id", return_value="123456789012"), \
         patch("sentinelcloud.core.orchestrator.COLLECTORS", fake):
        result = Orchestrator(Settings()).run(services=["s3"])
    assert result.account_id == "123456789012"
    assert len(result.findings) == 3
