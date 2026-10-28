#!/usr/bin/env python3
"""Executa o SentinelCloud sem instalar nada e sem internet.

Usa o codigo em ``src/`` e as dependencias embutidas em ``vendor/``.

    python run.py            # abre o assistente
    python run.py demo       # relatorio de exemplo
    python run.py scan --profile meu-perfil
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

if sys.version_info < (3, 10):
    sys.exit("E preciso Python 3.10 ou superior. Versao atual: " + sys.version.split()[0])

for sub in ("vendor", "src", ""):
    path = os.path.join(BASE, sub) if sub else BASE
    if os.path.isdir(path) and path not in sys.path:
        sys.path.insert(0, path)

from apps.cli.main import main  # noqa: E402

if __name__ == "__main__":
    args = sys.argv[1:] or ["start"]
    sys.exit(main(args))
