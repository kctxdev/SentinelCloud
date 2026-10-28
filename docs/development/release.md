# Release

1. Atualize a versao em `pyproject.toml` e `src/sentinelcloud/__init__.py`.
2. `python scripts/run_tests.py`
3. `python scripts/build.py`
4. Crie a tag `vX.Y.Z`: o workflow `release.yml` publica os artefatos.
