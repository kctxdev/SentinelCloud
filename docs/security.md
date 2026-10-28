# Seguranca

- A ferramenta e **somente leitura**: nenhuma chamada altera recursos.
- Segredos nunca sao gravados em logs (`security/redaction.py`).
- Nao versione `.env`; use `.env.example` como modelo.
- Relatorios podem conter nomes de recursos: trate-os como informacao sensivel.
- Reporte vulnerabilidades de forma privada aos mantenedores.
