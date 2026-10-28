"""Implementacao dos comandos."""
import sys

from sentinelcloud import __version__
from sentinelcloud.config import Settings
from sentinelcloud.core.orchestrator import Orchestrator
from sentinelcloud.core.severity import Severity
from sentinelcloud.demo import run_demo
from sentinelcloud.exceptions import SentinelError
from sentinelcloud.notifications.dispatcher import dispatch
from sentinelcloud.reports.csv_report import render_csv
from sentinelcloud.reports.json_report import render_json
from sentinelcloud.reports.terminal_report import render_terminal
from sentinelcloud.rules.registry import load_rules

from .output import emit, error


def cmd_version(args) -> int:
    print(f"SentinelCloud {__version__} - desenvolvido por {__author__}")
    return 0


def cmd_rules(args) -> int:
    for r in load_rules():
        print(f"{r.id:<9} {r.service:<11} {r.title}")
    return 0


def cmd_scan(args) -> int:
    settings = Settings.from_env()
    try:
        result = Orchestrator(settings).run(args.profile, args.region, args.services)
    except SentinelError as exc:
        error(str(exc))
        return 1

    if args.format == "json":
        text = render_json(result)
    elif args.format == "csv":
        text = render_csv(result)
    else:
        text = render_terminal(result, color=not args.no_color and not args.output and sys.stdout.isatty())
    emit(text, args.output)

    if args.notify:
        try:
            dispatch(settings, result, args.notify)
        except Exception as exc:
            error(f"falha ao notificar: {exc}")

    if args.fail_on:
        limit = Severity.parse(args.fail_on)
        if any(f.severity >= limit for f in result.findings):
            return 2
    return 0


def cmd_demo(args) -> int:
    """Relatorio de exemplo com dados ficticios, sem acessar a AWS."""
    result = run_demo()
    if args.format == "json":
        text = render_json(result)
    elif args.format == "csv":
        text = render_csv(result)
    else:
        text = render_terminal(result, color=not args.no_color and sys.stdout.isatty())
        text += "\n\n(DEMO: dados ficticios. Para escanear sua conta: sentinelcloud scan --profile SEU_PERFIL)"
    emit(text)
    return 0


def cmd_start(args) -> int:
    """Assistente interativo: pergunta como acessar a AWS e guia ate o relatorio."""
    from .wizard import Wizard

    return Wizard().run()


HANDLERS = {"start": cmd_start, "scan": cmd_scan, "demo": cmd_demo,
            "rules": cmd_rules, "version": cmd_version}
