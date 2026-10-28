"""Regras de seguranca.

Cada regra e uma funcao pura (recebe dicts ja coletados e devolve
``Finding``) registrada com o decorator ``@rule``. Para registrar uma nova
regra, crie o modulo e adicione-o em ``registry._MODULES``.
"""
from .registry import Rule, load_rules, rule
from .engine import RuleEngine

__all__ = ["Rule", "rule", "load_rules", "RuleEngine"]
