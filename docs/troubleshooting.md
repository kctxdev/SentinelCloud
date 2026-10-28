# Solucao de problemas

- **Credenciais invalidas**: confira `AWS_PROFILE` e rode `aws sts get-caller-identity`.
- **AccessDenied**: faltam permissoes; veja `docs/permissions.md`.
- **ModuleNotFoundError: apps**: rode a partir da raiz do projeto ou instale com `pip install -e .`.
- **Coleta vazia**: use `-v` para ver avisos de coleta.
