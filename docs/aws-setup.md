# Configuracao da AWS

1. Crie um usuario/role dedicado com a politica de `docs/permissions.md`.
2. Configure um perfil: `aws configure --profile sentinel` (ou use AWS SSO).
3. Execute: `sentinelcloud scan --profile sentinel`.

Prefira credenciais temporarias (SSO/AssumeRole) a chaves de longa duracao.
