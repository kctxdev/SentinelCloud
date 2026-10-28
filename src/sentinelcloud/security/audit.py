"""Trilha de auditoria local (somente metadados, sem segredos)."""
import json
import logging
from datetime import datetime, timezone

from .redaction import redact

_log = logging.getLogger("sentinelcloud.audit")


def audit_event(event: str, **fields) -> None:
    record = {"ts": datetime.now(timezone.utc).isoformat(), "event": event, **fields}
    _log.info(redact(json.dumps(record, default=str)))
