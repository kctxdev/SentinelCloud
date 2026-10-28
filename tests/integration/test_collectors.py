import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skip(reason="requer credenciais AWS reais")
def test_collectors_return_lists():
    from sentinelcloud.aws.collectors import COLLECTORS
    from sentinelcloud.aws.session import create_session

    session = create_session()
    for collect in COLLECTORS.values():
        assert isinstance(collect(session), list)
