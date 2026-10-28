import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skip(reason="requer credenciais AWS reais")
def test_session_identity():
    from sentinelcloud.aws.account import get_account_id
    from sentinelcloud.aws.session import create_session

    assert get_account_id(create_session())
