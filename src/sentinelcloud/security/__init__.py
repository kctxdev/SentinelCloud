"""Seguranca da propria ferramenta: mascaramento de segredos e auditoria."""
from .audit import audit_event
from .redaction import redact

__all__ = ["redact", "audit_event"]
