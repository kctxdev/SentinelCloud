from sentinelcloud.core.finding import Finding
from sentinelcloud.core.risk_engine import risk_rating, risk_score
from sentinelcloud.core.severity import Severity


def _f(sev):
    return Finding("X", "t", sev, "r", "d")


def test_score_and_cap():
    assert risk_score([]) == 0
    assert risk_score([_f(Severity.LOW), _f(Severity.HIGH)]) == 10
    assert risk_score([_f(Severity.CRITICAL)] * 10) == 100


def test_rating():
    assert risk_rating(0) == "NONE"
    assert risk_rating(5) == "LOW"
    assert risk_rating(100) == "CRITICAL"
