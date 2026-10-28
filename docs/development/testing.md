# Testes

```bash
pytest                      # unitarios, CLI e pipeline com mocks
pytest -m integration       # exige credenciais AWS (hoje marcados como skip)
pytest --cov=sentinelcloud
```

Fixtures JSON ficam em `tests/fixtures/`.
