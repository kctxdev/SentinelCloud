"""Geracao de relatorios: terminal, JSON e CSV, alem do resumo."""
from .csv_report import render_csv
from .json_report import render_json
from .summary import build_summary
from .terminal_report import render_terminal

__all__ = ["render_terminal", "render_json", "render_csv", "build_summary"]
