"""Gera sdist e wheel em dist/."""
import subprocess
import sys

sys.exit(subprocess.call([sys.executable, "-m", "build"]))
