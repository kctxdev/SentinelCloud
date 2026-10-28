# Uso

```bash
sentinelcloud scan --profile prod --region sa-east-1
sentinelcloud scan --services s3 iam
sentinelcloud scan --format json --output relatorio.json
sentinelcloud scan --notify telegram email
sentinelcloud scan --fail-on high     # codigo de saida 2 se houver HIGH/CRITICAL
sentinelcloud rules
```

Codigos de saida: `0` ok, `1` erro, `2` achados acima do limite (`--fail-on`).
