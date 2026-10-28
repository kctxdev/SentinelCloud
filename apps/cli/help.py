"""Textos de ajuda."""

DESCRIPTION = "SentinelCloud - scanner de seguranca para AWS (somente leitura)."

EPILOG = """exemplos:
  sentinelcloud start                     (assistente interativo, passo a passo)
  sentinelcloud demo                      (relatorio de exemplo, sem precisar de AWS)
  sentinelcloud scan --profile prod --region us-east-1
  sentinelcloud scan --services s3 iam --format json --output relatorio.json
  sentinelcloud scan --fail-on high
  sentinelcloud rules
"""
