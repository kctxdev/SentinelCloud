from unittest.mock import patch

from sentinelcloud.config import Settings
from sentinelcloud.core.orchestrator import Orchestrator
from sentinelcloud.exceptions import CollectionError
from sentinelcloud.reports.terminal_report import render_terminal


def _fail(session):
    raise CollectionError("CloudTrail: AccessDenied")


def test_failed_collection_does_not_create_false_findings():
    """Sem permissao no CloudTrail NAO pode virar o achado 'nenhuma trilha'."""
    fake = {"cloudtrail": _fail}
    with patch("sentinelcloud.core.orchestrator.get_account_id", return_value="1"), \
         patch("sentinelcloud.core.orchestrator.COLLECTORS", fake):
        result = Orchestrator(Settings()).run(services=["cloudtrail"], session=object())
    assert result.findings == []
    assert "cloudtrail" in result.errors
    text = render_terminal(result, color=False)
    assert "ATENCAO" in text and "Bom trabalho" not in text
