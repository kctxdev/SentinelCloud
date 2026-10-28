"""Niveis de severidade."""
from __future__ import annotations

from enum import IntEnum


class Severity(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @property
    def weight(self) -> int:
        return {1: 1, 2: 4, 3: 9, 4: 16}[int(self)]

    @classmethod
    def parse(cls, value: str) -> "Severity":
        try:
            return cls[value.strip().upper()]
        except KeyError as exc:
            raise ValueError(f"Severidade invalida: {value!r}") from exc
