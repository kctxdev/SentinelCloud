"""Saida da CLI."""
import sys


def emit(text: str, path: str | None = None) -> None:
    if path:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Relatorio salvo em {path}", file=sys.stderr)
    else:
        print(text)


def error(message: str) -> None:
    print(f"erro: {message}", file=sys.stderr)
