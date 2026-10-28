"""Coleta configuracoes de buckets S3."""
from __future__ import annotations

from ...exceptions import CollectionError


def _code(exc) -> str:
    return getattr(exc, "response", {}).get("Error", {}).get("Code", "")


def collect_s3(session) -> list[dict]:
    s3 = session.client("s3")
    try:
        buckets = s3.list_buckets().get("Buckets", [])
    except Exception as exc:
        raise CollectionError(f"S3: {exc}") from exc

    out = []
    for b in buckets:
        name = b["Name"]
        item = {"name": name, "public_access_block": None, "encryption": None, "logging": False}
        try:
            item["public_access_block"] = s3.get_public_access_block(Bucket=name)[
                "PublicAccessBlockConfiguration"
            ]
        except Exception as exc:
            if _code(exc) != "NoSuchPublicAccessBlockConfiguration":
                item["error"] = str(exc)
        try:
            rules = s3.get_bucket_encryption(Bucket=name)["ServerSideEncryptionConfiguration"]["Rules"]
            item["encryption"] = rules[0]["ApplyServerSideEncryptionByDefault"]
        except Exception as exc:
            if _code(exc) != "ServerSideEncryptionConfigurationNotFoundError":
                item["error"] = str(exc)
        try:
            item["logging"] = "LoggingEnabled" in s3.get_bucket_logging(Bucket=name)
        except Exception as exc:
            item["error"] = str(exc)
        out.append(item)
    return out
