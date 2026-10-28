"""Definicao dos argumentos da CLI."""
import argparse

from .help import DESCRIPTION, EPILOG


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinelcloud", description=DESCRIPTION, epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="logs detalhados")
    sub = parser.add_subparsers(dest="command")

    scan = sub.add_parser("scan", help="executa o scan na conta AWS")
    scan.add_argument("--profile", help="perfil AWS (padrao: AWS_PROFILE)")
    scan.add_argument("--region", help="regiao AWS (padrao: AWS_REGION)")
    scan.add_argument("--services", nargs="+", choices=["s3", "ec2", "iam", "cloudtrail"])
    scan.add_argument("--format", choices=["terminal", "json", "csv"], default="terminal")
    scan.add_argument("--output", help="arquivo de saida (padrao: stdout)")
    scan.add_argument("--notify", nargs="+", choices=["telegram", "email"], help="canais de notificacao")
    scan.add_argument("--fail-on", choices=["low", "medium", "high", "critical"],
                      help="retorna codigo 2 se houver achado >= severidade")
    scan.add_argument("--no-color", action="store_true")

    sub.add_parser("start", help="assistente interativo (recomendado para o primeiro uso)")

    demo = sub.add_parser("demo", help="mostra um relatorio de exemplo (sem AWS)")
    demo.add_argument("--format", choices=["terminal", "json", "csv"], default="terminal")
    demo.add_argument("--no-color", action="store_true")

    sub.add_parser("rules", help="lista as regras disponiveis")
    sub.add_parser("version", help="mostra a versao")
    return parser
