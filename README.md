# SentinelCloud

**Scanner de segurança para contas AWS.** O SentinelCloud olha as configurações da sua conta, procura erros comuns de segurança (um bucket aberto ao público, uma porta SSH liberada para o mundo inteiro, uma política de administrador solta por aí...) e entrega um relatório claro dizendo **o que está errado, onde está e como corrigir**.

Ele foi feito para ser usado por qualquer pessoa: basta dar duplo clique em um arquivo e responder às perguntas que aparecem no terminal.

> **Somente leitura.** O SentinelCloud só consulta configurações. Ele nunca cria, altera ou apaga nada na conta AWS, e não escaneia o computador onde está rodando. Use apenas em contas que você tem autorização para auditar.

---

## Sumário

1. [Começando em 3 minutos](#começando-em-3-minutos)
2. [Executar no Windows](#executar-no-windows)
3. [O assistente passo a passo](#o-assistente-passo-a-passo)
4. [Todos os comandos](#todos-os-comandos)
5. [O que ele verifica](#o-que-ele-verifica)
6. [Acesso à AWS e permissões](#acesso-à-aws-e-permissões)
7. [Exemplo de relatório](#exemplo-de-relatório)
8. [Usar em automação (CI/CD)](#usar-em-automação-cicd)
9. [Levar para outro computador](#levar-para-outro-computador)
10. [Segurança e privacidade](#segurança-e-privacidade)
11. [Problemas comuns](#problemas-comuns)
12. [Para desenvolvedores](#para-desenvolvedores)
13. [Autor](#autor)

---

## Começando em 3 minutos

**Você precisa de:** apenas o **Python 3.10 ou superior** instalado. **Não precisa de internet para abrir o programa nem instalar nada:** todas as dependências já vêm dentro da pasta `vendor/`. (A internet só é necessária, claro, para o scan falar com a AWS.)

### Opção A: duplo clique (mais fácil)

| Sistema | O que fazer |
|---------|-------------|
| **Windows** | Dê duplo clique em `iniciar.bat` |
| **Linux** | Abra um terminal na pasta e rode `./iniciar.sh` (ou `bash iniciar.sh`) |
| **macOS** | Abra o Terminal na pasta e rode `./iniciar.sh` |

> O `iniciar.sh` **não funciona no Windows**; lá use o `iniciar.bat`.
> No Linux, se aparecer "permissão negada", rode antes `chmod +x iniciar.sh`.
> Não tem Python? Windows: [python.org/downloads](https://www.python.org/downloads/) (marque "Add python.exe to PATH"). Ubuntu/Debian: `sudo apt install python3`.

### Opção B: rodar direto, sem instalar (qualquer sistema)

```bash
python run.py            # abre o assistente (no Windows pode ser: py run.py)
python run.py demo       # relatório de exemplo
python run.py scan --profile meu-perfil --region us-east-1
```

### Opção C: instalação como comando `sentinelcloud` (opcional, precisa de internet)

```bash
python3 -m venv .venv
source .venv/bin/activate          # fish: source .venv/bin/activate.fish
                                   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .

sentinelcloud start                # abre o assistente
```

### Quer só ver como é, sem conta AWS?

```bash
python run.py demo       # ou, se instalou o comando: sentinelcloud demo
```

Mostra um relatório completo com dados **fictícios**, para você conhecer a saída da ferramenta antes de usá-la numa conta de verdade.

---

## Executar no Windows

**1. Instale o Python (uma vez só)**

Baixe em [python.org/downloads](https://www.python.org/downloads/) e, na primeira tela do instalador, **marque a caixa "Add python.exe to PATH"** antes de clicar em *Install Now*. Para conferir, abra o PowerShell e rode `python --version` (precisa mostrar 3.10 ou superior).

**2. Extraia o projeto**

Clique com o botão direito no `SentinelCloud.zip` e escolha **"Extrair tudo..."**. Não execute o programa de dentro do zip: ele precisa estar extraído numa pasta normal (por exemplo, `C:\Users\SeuNome\SentinelCloud`).

**3. Abra o assistente**

Dê duplo clique em **`iniciar.bat`**. Ele **não baixa nada e funciona sem internet**: usa as dependências que já estão na pasta `vendor/`. Abre uma janela preta onde o assistente faz as perguntas.

> Se o Windows mostrar *"O Windows protegeu o computador"* (SmartScreen), clique em **Mais informações** e depois em **Executar assim mesmo**. O aviso aparece porque o arquivo veio da internet e não tem assinatura digital.
> A janela fecha ao terminar, mas o `iniciar.bat` espera você apertar uma tecla antes, então dá tempo de ler o resultado.

**4. Configure o acesso à AWS (só para escanear uma conta de verdade)**

- Instale o AWS CLI: [docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Abra o PowerShell e rode `aws configure --profile sentinel`.
- No assistente, escolha **"Usar um perfil AWS salvo neste computador"**. Se preferir não instalar o AWS CLI, escolha **"Digitar chaves de acesso"** e informe as chaves ali mesmo.

**Pelo PowerShell (alternativa ao duplo clique)**

```powershell
cd C:\caminho\para\SentinelCloud
python run.py          # ou: py run.py
```

Não precisa de ambiente virtual nem de `pip install`.

**Problemas comuns no Windows**

| Sintoma | O que fazer |
|---------|-------------|
| `Python 3.10 ou superior nao foi encontrado` | Reinstale o Python marcando "Add python.exe to PATH" |
| A janela abre e fecha na hora | Você está dentro do zip. Extraia o projeto primeiro |
| `A pasta "vendor" nao foi encontrada` | O projeto não foi extraído por inteiro. Extraia o `.zip` completo e tente de novo |
| `.sh` não abre no Windows | Normal: use o `iniciar.bat` (o `.sh` é só para Linux/macOS) |
| Antivírus bloqueia o `.bat` | Libere a pasta do projeto ou rode pelo PowerShell, como acima |
| Caracteres estranhos no relatório | Use o **Windows Terminal** (ou rode `chcp 65001` antes) |

---

## O assistente passo a passo

O assistente (`iniciar.sh`, `iniciar.bat` ou `sentinelcloud start`) conduz tudo por perguntas:

1. **Como acessar a conta AWS?**
   - *Perfil salvo neste computador* (recomendado): usa um perfil já configurado em `~/.aws`.
   - *Digitar chaves de acesso*: você informa Access Key e Secret; a senha não aparece enquanto você digita. As chaves ficam **só na memória** e são descartadas ao terminar.
   - *Credenciais padrão do ambiente*: usa AWS SSO, variáveis `AWS_*` ou uma role do ambiente.
   - *Demonstração*: dados fictícios, sem AWS.
2. **Qual região?** (padrão: `us-east-1` ou o valor de `AWS_REGION`)
3. **Confirmação da conta.** O programa mostra o número da conta e a identidade conectada e pergunta *"Esta é a conta que você quer escanear?"*. Se você responder não, nada é escaneado.
4. **Quais serviços?** Todos (S3, EC2, IAM, CloudTrail) ou só alguns.
5. **Scan e resultado** direto no terminal, do achado mais grave ao menos grave.
6. **Salvar o relatório?** Opcional, em JSON ou CSV.

A qualquer momento, **Ctrl+C** cancela sem alterar nada.

Se algum serviço não puder ser lido (normalmente falta de permissão), o relatório avisa que ficou **incompleto**, em vez de inventar problemas que não existem.

---

## Todos os comandos

| Comando | O que faz |
|---------|-----------|
| `sentinelcloud start` | Assistente interativo, passo a passo (recomendado) |
| `sentinelcloud demo` | Relatório de exemplo com dados fictícios (aceita `--format json` e `csv`) |
| `sentinelcloud scan` | Scan direto, para quem prefere comandos ou automação |
| `sentinelcloud rules` | Lista as regras de segurança |
| `sentinelcloud version` | Mostra a versão |

### Opções do `scan`

| Opção | O que faz |
|-------|-----------|
| `--profile` | Perfil AWS a usar (padrão: variável `AWS_PROFILE`) |
| `--region` | Região AWS (padrão: `AWS_REGION`, ou `us-east-1`) |
| `--services` | Limita o scan a `s3`, `ec2`, `iam` e/ou `cloudtrail` |
| `--format` | `terminal` (padrão), `json` ou `csv` |
| `--output` | Salva o relatório neste arquivo em vez de imprimir |
| `--notify` | Envia um resumo por `telegram` e/ou `email` (veja `.env.example`) |
| `--fail-on` | `low`, `medium`, `high` ou `critical`: retorna código `2` se houver achado igual ou pior |
| `--no-color` | Desativa as cores |
| `-v` | Logs detalhados (útil para depurar) |

Exemplos:

```bash
sentinelcloud scan --profile sentinel --region sa-east-1
sentinelcloud scan --services s3 iam --format json --output relatorio.json
sentinelcloud scan --format csv --output relatorio.csv
```

### Códigos de saída

| Código | Significado |
|--------|-------------|
| `0` | Tudo certo |
| `1` | Erro (credenciais inválidas, falha de configuração etc.) |
| `2` | Há achados acima do limite definido em `--fail-on` |
| `130` | Cancelado pelo usuário (Ctrl+C) no assistente |

---

## O que ele verifica

| Regra | Serviço | Severidade | O que detecta |
|-------|---------|-----------|---------------|
| `S3-001` | S3 | Alta | Bucket sem o bloqueio completo de acesso público (as 4 opções do *Block Public Access*) |
| `S3-002` | S3 | Média | Bucket sem criptografia padrão em repouso |
| `S3-003` | S3 | Baixa | Bucket sem log de acesso |
| `EC2-001` | EC2 | Alta / Crítica | Security Group que libera para a internet (`0.0.0.0/0` ou `::/0`) portas sensíveis (SSH, RDP, MySQL, PostgreSQL, MSSQL, Redis, MongoDB, Elasticsearch) ou **todo** o tráfego |
| `IAM-001` | IAM | Média / Alta / Crítica | Políticas com permissões excessivas: `*` em tudo (admin total), `Action: *`, ou `servico:*` em todos os recursos |
| `CT-001` | CloudTrail | Alta / Média | Nenhuma trilha configurada, trilha parada, ou nenhuma trilha multi-região |

### Pontuação de risco

Cada achado soma pontos conforme a severidade, e o total é limitado a 100:

| Severidade | Pontos |
|-----------|--------|
| Baixa | 1 |
| Média | 4 |
| Alta | 9 |
| Crítica | 16 |

Classificação final: **NONE** (0), **LOW** (1–9), **MEDIUM** (10–29), **HIGH** (30–59) e **CRITICAL** (60 ou mais).

---

## Acesso à AWS e permissões

O SentinelCloud precisa apenas de permissões de **leitura**. Crie um usuário ou role dedicado com a política abaixo (a mesma está em [`docs/permissions.md`](docs/permissions.md)):

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "sts:GetCallerIdentity",
      "s3:ListAllMyBuckets", "s3:GetBucketPublicAccessBlock",
      "s3:GetEncryptionConfiguration", "s3:GetBucketLogging",
      "ec2:DescribeSecurityGroups",
      "iam:ListPolicies", "iam:GetPolicyVersion",
      "cloudtrail:DescribeTrails", "cloudtrail:GetTrailStatus"
    ],
    "Resource": "*"
  }]
}
```

Para criar um perfil no computador:

```bash
aws configure --profile sentinel
```

Prefira credenciais temporárias (AWS SSO ou AssumeRole) a chaves de longa duração. Nunca coloque chaves dentro do código ou do repositório.

---

## Exemplo de relatório

```
============================================================
SentinelCloud - conta 123456789012 (DEMO) (us-east-1)
============================================================
Achados: 12 | Risco: 91/100 (CRITICAL)
  CRITICAL: 2  HIGH: 5  MEDIUM: 3  LOW: 2

[CRITICAL] EC2-001 sg-8c9d0e1f (tudo-liberado) - Todo o trafego liberado para a internet
    Regra de entrada com protocolo -1 aberta para 0.0.0.0/0 ou ::/0.
    Correcao: Restrinja a origem e as portas ao minimo necessario.
[CRITICAL] IAM-001 AdminTotal - Politica IAM com permissoes excessivas
    Permite todas as acoes em todos os recursos (acesso administrativo).
    Correcao: Aplique o principio do menor privilegio: limite acoes e recursos.
[HIGH] S3-001 empresa-backups-publico - Bucket sem bloqueio completo de acesso publico
    Configuracoes ausentes/desativadas: BlockPublicAcls, IgnorePublicAcls, ...
    Correcao: Ative as 4 opcoes de S3 Block Public Access no bucket e na conta.
...
```

Para cada achado você vê a **regra**, o **recurso afetado**, a **explicação** e a **correção sugerida**.

---

## Usar em automação (CI/CD)

```bash
sentinelcloud scan --profile sentinel --fail-on high
```

Retorna código de saída `2` se existir algum achado de severidade **alta ou superior**, o que permite bloquear um deploy automaticamente.

---

## Levar para outro computador

1. Copie a pasta (ou o `.zip`) do projeto para a outra máquina e extraia.
2. Garanta Python 3.10+ instalado lá.
3. Dê duplo clique em `iniciar.sh` (Linux/macOS) ou `iniciar.bat` (Windows).

As credenciais AWS ficam **sempre na máquina de quem usa**; elas nunca fazem parte do projeto. Para um scan real, a pessoa configura o próprio acesso (perfil, SSO ou chaves digitadas no assistente).

---

## Segurança e privacidade

- **Somente leitura:** nenhuma chamada da ferramenta modifica recursos da AWS.
- **Nada é enviado para terceiros:** os dados do scan ficam no computador. A única saída de rede além da AWS é a notificação por Telegram ou e-mail, e só se você a ativar.
- **Chaves digitadas ficam só na memória:** não são gravadas em arquivo nem em logs. Segredos, senhas e tokens também são mascarados automaticamente nos logs.
- **Confirmação da conta:** o assistente mostra qual conta está conectada antes de escanear.
- **Relatórios são sensíveis:** eles listam nomes de buckets, grupos de segurança e políticas. Guarde-os com cuidado e não os publique.
- **Auditoria:** cada scan registra início e fim (conta, região, quantidade de achados), sem dados secretos.

Mais detalhes em [`docs/security.md`](docs/security.md).

---

## Problemas comuns

| Mensagem / sintoma | O que fazer |
|--------------------|-------------|
| `Python 3.10 ou superior nao foi encontrado` | Instale o Python (veja [Começando](#começando-em-3-minutos)) |
| `python3 -m venv` falha no Ubuntu/Debian | `sudo apt install python3-venv` |
| `Could not open requirements file: requirements.txt` | Você não está na pasta do projeto. Entre na pasta que contém `run.py` e `pyproject.toml` |
| `sentinelcloud: command not found` | Você não instalou o comando (Opção C). Use `python run.py` ou `iniciar.sh`/`iniciar.bat` |
| Erro de `case ... nao esta dentro de um bloco switch` ao ativar | Você usa o shell **fish**: use `source .venv/bin/activate.fish` |
| `pip install -e` mostra "requires 1 argument" | Faltou o ponto no final: `pip install -e .` |
| Credenciais inválidas ou ausentes | Confira o perfil: `aws sts get-caller-identity --profile sentinel` |
| `AccessDenied` / relatório marcado como **incompleto** | Faltam permissões; use a política da seção [Acesso à AWS](#acesso-à-aws-e-permissões) |
| O assistente não lista nenhum perfil | Nenhum perfil em `~/.aws`; crie com `aws configure --profile sentinel` ou escolha outra opção do menu |

Mais casos em [`docs/troubleshooting.md`](docs/troubleshooting.md). Use `-v` nos comandos para ver detalhes de qualquer falha.

---

## Para desenvolvedores

### Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Resultado esperado: `24 passed, 2 skipped`. Os testes usam dados de exemplo (`tests/fixtures/`) e **não** acessam a AWS; os 2 ignorados são testes de integração que exigem credenciais reais.

### Estrutura do projeto

```
apps/cli/                 Interface de linha de comando (comandos, argumentos e assistente)
src/sentinelcloud/
  core/                   Scanner, orquestrador, modelo de achado, severidade e pontuação de risco
  aws/                    Autenticação, sessão e coletores (S3, Security Groups, IAM, CloudTrail)
  rules/                  Regras de segurança (uma por arquivo, agrupadas por serviço)
  reports/                Relatórios em terminal, JSON e CSV
  notifications/          Envio por Telegram e e-mail
  security/               Mascaramento de segredos e auditoria
  utils/                  Logging, retry e paginação
  demo.py                 Dados fictícios do comando demo
tests/                    Testes unitários, de integração e da CLI
docs/                     Documentação detalhada
scripts/                  Build, empacotamento e execução de testes
iniciar.sh / iniciar.bat  Iniciadores (Linux/macOS e Windows), funcionam sem internet
run.py                    Executa o programa direto, sem instalar
vendor/                   Dependências embutidas (boto3 e afins), para uso offline
```

Como as peças se conectam: a CLI (ou o assistente) chama o **orquestrador**, que usa a **sessão AWS** e os **coletores** para obter os dados; o **scanner** aplica as **regras** sobre esses dados; e os **relatórios** (e **notificações**) apresentam o resultado. As regras não falam com a AWS, por isso são fáceis de testar.

### Criar uma nova regra

1. Crie um módulo em `src/sentinelcloud/rules/<servico>/`.
2. Decore a função com `@rule(id, servico, titulo)`; ela recebe a lista de recursos coletados e devolve uma lista de `Finding`.
3. Adicione o módulo em `_MODULES` (`rules/registry.py`) e escreva testes.

### Documentação

| Documento | Conteúdo |
|-----------|----------|
| [`docs/architecture.md`](docs/architecture.md) | Como o projeto é organizado |
| [`docs/installation.md`](docs/installation.md) | Instalação passo a passo |
| [`docs/usage.md`](docs/usage.md) | Exemplos de uso |
| [`docs/aws-setup.md`](docs/aws-setup.md) | Preparando a conta AWS |
| [`docs/permissions.md`](docs/permissions.md) | Política IAM somente leitura necessária |
| [`docs/rules.md`](docs/rules.md) | Lista de regras e como criar uma nova |
| [`docs/security.md`](docs/security.md) | Práticas de segurança |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | Solução de problemas |
| [`docs/development/`](docs/development) | Contribuição, testes e releases |

---

## Autor

Desenvolvido por **kactxn.dev**
Cloud & DevSecOps · AWS · Terraform · Segurança da Informação

- GitHub: [github.com/kctxdev](https://github.com/kctxdev)

---

## Licença

MIT © 2026 kactxn.dev. Veja o arquivo [`LICENSE`](LICENSE).