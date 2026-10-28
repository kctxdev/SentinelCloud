"""Coleta trilhas do CloudTrail."""
from __future__ import annotations

from ...exceptions import CollectionError


def collect_cloudtrail(session) -> list[dict]:
    ct = session.client("cloudtrail")
    try:
        trails = ct.describe_trails(includeShadowTrails=False).get("trailList", [])
        out = []
        for t in trails:
            status = ct.get_trail_status(Name=t["TrailARN"])
            out.append({
                "name": t["Name"],
                "is_logging": bool(status.get("IsLogging")),
                "multi_region": bool(t.get("IsMultiRegionTrail")),
            })
        return out
    except Exception as exc:
        raise CollectionError(f"CloudTrail: {exc}") from exc
