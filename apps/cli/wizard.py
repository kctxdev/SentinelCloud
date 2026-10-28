"""Assistente interativo: guia a pessoa passo a passo ate o relatorio.

Uso: ``sentinelcloud start`` (ou o arquivo iniciar.sh / iniciar.bat).

Fluxo: escolher como acessar a AWS -> confirmar a conta -> escolher servicos
-> escanear -> ver o resultado -> (opcional) salvar relatorio.
As chaves digitadas ficam somente na memoria; nunca sao gravadas.
"""
from __future__ import annotations

import getpass
import os
import sys
from datetime import datetime

from sentinelcloud import __version__
from sentinelcloud.aws.authentication import caller_identity
from sentinelcloud.aws.session import create_session, list_profiles
from sentinelcloud.core.orchestrator import SERVICES, Orchestrator
from sentinelcloud.demo import run_demo
from sentinelcloud.exceptions import SentinelError
from sentinelcloud.reports.csv_report import render_csv
from sentinelcloud.reports.json_report import render_json
from sentinelcloud.reports.terminal_report import render_terminal

BANNER = """
============================================================
 SentinelCloud {version} - assistente de seguranca para AWS
============================================================
Este programa analisa a configuracao de uma conta AWS e aponta
riscos de seguranca (S3, Security Groups, IAM e CloudTrail).

  * SOMENTE LEITURA: nada na conta e criado, alterado ou apagado.
  * Use apenas em contas que voce tem autorizacao para auditar.
  * Para cancelar a qualquer momento, aperte Ctrl+C.
"""

KEYS_NOTICE = """
  Dica: use chaves de um usuario com permissao SOMENTE LEITURA
  (veja docs/permissions.md). As chaves nao sao gravadas em disco nem
  em logs; so existem enquanto este programa estiver aberto.
"""

SERVICE_LABELS = {
    "s3": "S3 (buckets)",
    "ec2": "EC2 (Security Groups)",
    "iam": "IAM (politicas)",
    "cloudtrail": "CloudTrail (auditoria)",
}


class Wizard:
    def __init__(self, input_fn=input, secret_fn=getpass.getpass, out=print,
                 profiles_fn=list_profiles, session_factory=create_session,
                 identity_fn=caller_identity, scan_fn=None, color=None):
        self.input_fn = input_fn
        self.secret_fn = secret_fn
        self.out = out
        self.profiles_fn = profiles_fn
        self.session_factory = session_factory
        self.identity_fn = identity_fn
        self.scan_fn = scan_fn or self._default_scan
        self.color = sys.stdout.isatty() if color is None else color

    # ------------------------------------------------------------ helpers
    @staticmethod
    def _default_scan(session, region, services):
        return Orchestrator().run(region=region, services=services, session=session)

    def ask(self, prompt: str, default: str | None = None) -> str:
        suffix = f" [{default}]" if default else ""
        text = self.input_fn(f"{prompt}{suffix}: ").strip()
        return text or (default or "")

    def yes_no(self, prompt: str, default: bool = True) -> bool:
        hint = "S/n" if default else "s/N"
        while True:
            text = self.input_fn(f"{prompt} [{hint}]: ").strip().lower()
            if not text:
                return default
            if text in ("s", "sim", "y", "yes"):
                return True
            if text in ("n", "nao", "não", "no"):
                return False
            self.out("  Responda com s (sim) ou n (nao).")

    def choose(self, title: str, options: list[str]) -> int:
        """Mostra opcoes numeradas e devolve o numero escolhido (1-based)."""
        self.out(f"\n{title}")
        for i, option in enumerate(options, 1):
            self.out(f"  {i}) {option}")
        while True:
            text = self.input_fn(f"Escolha 1-{len(options)}: ").strip()
            if text.isdigit() and 1 <= int(text) <= len(options):
                return int(text)
            self.out("  Opcao invalida.")

    # --------------------------------------------------------------- flow
    def run(self) -> int:
        try:
            return self._flow()
        except (KeyboardInterrupt, EOFError):
            self.out("\nCancelado. Nada foi alterado na conta.")
            return 130
        except SentinelError as exc:
            self.out(f"\nErro: {exc}")
            self.out("Confira as credenciais/permissoes (veja docs/troubleshooting.md).")
            return 1

    def _flow(self) -> int:
        self.out(BANNER.format(version=__version__))
        mode, kwargs = self._choose_access()
        if mode == "demo":
            return self._demo()

        region = self.ask("Regiao AWS", os.environ.get("AWS_REGION", "us-east-1"))
        self.out("\nConectando a AWS...")
        session = self.session_factory(region=region, **kwargs)
        identity = self.identity_fn(session)
        kwargs.clear()  # descarta as chaves digitadas

        self.out("Conectado com sucesso.")
        self.out(f"  Conta:      {identity.get('Account', '?')}")
        self.out(f"  Identidade: {identity.get('Arn', '?')}")
        if not self.yes_no("\nEsta e a conta que voce quer escanear?"):
            self.out("Tudo bem. Nada foi escaneado.")
            return 0

        services = self._choose_services()
        self.out("\nEscaneando... (somente leitura; pode levar alguns segundos)")
        result = self.scan_fn(session, region, services)
        self._show(result)
        self._offer_save(result)
        return 0

    def _choose_access(self) -> tuple[str, dict]:
        while True:
            method = self.choose("Como voce quer acessar a conta AWS?", [
                "Usar um perfil AWS salvo neste computador (recomendado)",
                "Digitar chaves de acesso (ficam so na memoria, nao sao salvas)",
                "Usar as credenciais padrao do ambiente (SSO, variaveis AWS_*, role)",
                "Ver uma DEMONSTRACAO com dados ficticios (sem AWS)",
            ])
            if method == 4:
                return "demo", {}
            if method == 1:
                profiles = self.profiles_fn()
                if not profiles:
                    self.out("  Nenhum perfil AWS encontrado neste computador (~/.aws).")
                    self.out("  Escolha outra opcao, ou rode 'aws configure' antes.")
                    continue
                idx = self.choose("Qual perfil?", profiles)
                return "aws", {"profile": profiles[idx - 1]}
            if method == 2:
                self.out(KEYS_NOTICE)
                key = self.ask("Access Key ID").strip()
                secret = self.secret_fn(
                    "Secret Access Key (nao aparece enquanto voce digita): ").strip()
                token = self.secret_fn(
                    "Session Token (opcional; Enter para pular): ").strip()
                if not key or not secret:
                    self.out("  Access Key ID e Secret Access Key sao obrigatorios.")
                    continue
                return "aws", {"access_key": key, "secret_key": secret,
                               "session_token": token or None}
            return "aws", {}

    def _choose_services(self) -> list[str]:
        if self.yes_no("Escanear todos os servicos (S3, EC2, IAM e CloudTrail)?"):
            return list(SERVICES)
        self.out("\nServicos disponiveis:")
        for i, name in enumerate(SERVICES, 1):
            self.out(f"  {i}) {SERVICE_LABELS.get(name, name)}")
        while True:
            text = self.ask("Digite os numeros separados por virgula (ex.: 1,3)")
            parts = [p.strip() for p in text.split(",") if p.strip()]
            if parts and all(p.isdigit() and 1 <= int(p) <= len(SERVICES) for p in parts):
                return sorted({SERVICES[int(p) - 1] for p in parts}, key=SERVICES.index)
            self.out("  Entrada invalida.")

    def _show(self, result) -> None:
        self.out("\n" + render_terminal(result, color=self.color))

    def _demo(self) -> int:
        self._show(run_demo())
        self.out("\n(DEMONSTRACAO com dados ficticios. Rode de novo e escolha a opcao 1, 2 ou 3 "
                 "para escanear uma conta de verdade.)")
        return 0

    def _offer_save(self, result) -> None:
        choice = self.choose("Deseja salvar o relatorio em arquivo?",
                             ["Nao", "Sim, em JSON", "Sim, em CSV"])
        if choice == 1:
            return
        ext = "json" if choice == 2 else "csv"
        default = f"relatorio-{result.account_id}-{datetime.now():%Y%m%d-%H%M}.{ext}"
        path = self.ask("Nome do arquivo", default)
        text = render_json(result) if ext == "json" else render_csv(result)
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        except OSError as exc:
            self.out(f"Nao foi possivel salvar: {exc}")
            return
        self.out(f"Relatorio salvo em {os.path.abspath(path)}")
        self.out("Lembre-se: o relatorio lista recursos da conta. Guarde-o com cuidado.")
