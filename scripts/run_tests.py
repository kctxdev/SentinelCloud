"""Executa a suite de testes."""
import subprocess
import sys

sys.exit(subprocess.call([sys.executable, "-m", "pytest", "-q", *sys.argv[1:]]))
