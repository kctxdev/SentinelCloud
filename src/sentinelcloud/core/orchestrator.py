"""Orquestra autenticacao, coleta, scan e relatorios."""
from __future__ import annotations

import logging

from ..aws.account import get_account_id
from ..aws.collectors import COLLECTORS
from ..aws.session import create_session
from ..config import Settings
from ..exceptions import CollectionError
from ..security.audit import audit_event
from .scanner import Scanner, ScanResult

log = logging.getLogger(__name__)

SERVICES = list(COLLECTORS.keys())


class Orchestrator:
    def __init__(self, settings: Settings | None = None, scanner: Scanner | None = None):
        self.settings = settings or Settings.from_env()
        self.scanner = scanner or Scanner()

    def run(self, profile: str | None = None, region: str | None = None,
            services: list[str] | None = None, session=None) -> ScanResult:
        """Executa o scan. Se `session` for passada, ela e usada no lugar de criar uma."""
        region = region or self.settings.region
        services = services or SERVICES

        if session is None:
            session = create_session(profile or self.settings.profile, region)
        account_id = get_account_id(session)
        audit_event("scan_started", account=account_id, region=region, services=services)

        data: dict[str, list] = {}
        errors: dict[str, str] = {}
        for name in services:
            try:
                data[name] = COLLECTORS[name](session)
            except CollectionError as exc:
                # Nao grava lista vazia: evitaria falsos achados (ex.: "sem CloudTrail")
                log.warning("Coleta falhou para %s: %s", name, exc)
                errors[name] = str(exc)

        result = self.scanner.scan(data, services, account_id=account_id, region=region,
                                   errors=errors)
        audit_event("scan_finished", account=account_id, findings=len(result.findings))
        return result
