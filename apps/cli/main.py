"""Ponto de entrada da CLI."""
import sys

from sentinelcloud.utils.logging import setup_logging

from .arguments import build_parser
from .commands import HANDLERS


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(args.verbose)
    if not args.command:
        parser.print_help()
        return 0
    return HANDLERS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
