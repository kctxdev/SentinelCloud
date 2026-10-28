# Regras

| ID | Servico | Severidade | Descricao |
|----|---------|-----------|-----------|
| S3-001 | S3 | HIGH | Bucket sem bloqueio completo de acesso publico |
| S3-002 | S3 | MEDIUM | Bucket sem criptografia padrao |
| S3-003 | S3 | LOW | Bucket sem logs de acesso |
| EC2-001 | EC2 | HIGH/CRITICAL | Portas sensiveis ou todo o trafego abertos ao mundo |
| IAM-001 | IAM | MEDIUM/HIGH/CRITICAL | Permissoes excessivas (`*`) |
| CT-001 | CloudTrail | HIGH/MEDIUM | Trilha ausente, parada ou nao multi-regiao |

## Nova regra

1. Crie um modulo em `rules/<servico>/`.
2. Decore a funcao com `@rule(id, servico, titulo)`.
3. Adicione o modulo em `_MODULES` (`rules/registry.py`) e escreva testes.
