"""Coleta Security Groups do EC2."""
from __future__ import annotations

from ...exceptions import CollectionError
from ...utils.pagination import paginate


def collect_security_groups(session) -> list[dict]:
    ec2 = session.client("ec2")
    try:
        return list(paginate(ec2, "describe_security_groups", "SecurityGroups"))
    except Exception as exc:
        raise CollectionError(f"EC2: {exc}") from exc
