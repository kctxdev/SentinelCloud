"""Mascara segredos em textos e logs."""
import re

PATTERNS = [
    (re.compile(r"\b(AKIA|ASIA)[A-Z0-9]{16}\b"), "[REDACTED_AWS_KEY_ID]"),
    (re.compile(r"(?i)(aws_secret_access_key|secret[_-]?key|password|token)\s*[=:]\s*\S+"), r"\1=[REDACTED]"),
    (re.compile(r"\bbot\d+:[A-Za-z0-9_-]{20,}"), "bot[REDACTED]"),
]


def redact(text: str) -> str:
    for pattern, repl in PATTERNS:
        text = pattern.sub(repl, text)
    return text
