"""Empacota o conteudo de dist/ em um zip."""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
archive = shutil.make_archive(str(root / "sentinelcloud-dist"), "zip", root / "dist")
print(f"Criado: {archive}")
