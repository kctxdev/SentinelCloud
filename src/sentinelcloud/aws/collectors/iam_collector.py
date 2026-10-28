"""Coleta politicas IAM gerenciadas pelo cliente."""
from __future__ import annotations

from ...exceptions import CollectionError
from ...utils.pagination import paginate


def collect_iam(session) -> list[dict]:
    iam = session.client("iam")
    out = []
    try:
        for pol in paginate(iam, "list_policies", "Policies", Scope="Local", OnlyAttached=False):
            version = iam.get_policy_version(
                PolicyArn=pol["Arn"], VersionId=pol["DefaultVersionId"]
            )["PolicyVersion"]
            out.append({"name": pol["PolicyName"], "arn": pol["Arn"], "document": version["Document"]})
    except Exception as exc:
        raise CollectionError(f"IAM: {exc}") from exc
    return out
