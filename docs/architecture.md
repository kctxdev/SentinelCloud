# Arquitetura

```
CLI (apps/cli) -> Orchestrator -> Sessao AWS -> Collectors -> dados (dict)
                                                     |
                                   Scanner -> RuleEngine -> Rules -> Findings
                                                     |
                                      RiskEngine -> Reports -> Notificacoes
```

- **aws/**: autenticacao, sessao e coletores (somente leitura).
- **rules/**: regras puras (recebem dicts, retornam `Finding`), registradas por decorator.
- **core/**: modelos, scanner, motor de risco e orquestrador.
- **reports/**: terminal, JSON e CSV.
- **notifications/**: Telegram e e-mail.
- **security/**: redacao de segredos e auditoria.

Regras nao chamam a AWS: isso permite testa-las com fixtures JSON.
