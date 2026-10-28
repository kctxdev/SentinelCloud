from apps.cli.wizard import Wizard
from sentinelcloud.demo import run_demo


def make_wizard(answers, secrets=(), **kwargs):
    """Wizard com entradas simuladas; devolve (wizard, linhas_de_saida)."""
    answers, secrets, lines = iter(answers), iter(secrets), []
    wiz = Wizard(
        input_fn=lambda prompt: next(answers),
        secret_fn=lambda prompt: next(secrets),
        out=lines.append,
        color=False,
        **kwargs,
    )
    return wiz, lines


def test_demo_option_runs_without_aws():
    wiz, lines = make_wizard(["4"])
    assert wiz.run() == 0
    text = "\n".join(lines)
    assert "DEMONSTRACAO" in text and "S3-001" in text


def test_keys_flow_scans_and_never_prints_secret():
    created = {}

    def fake_session(**kw):
        created.update(kw)
        return object()

    wiz, lines = make_wizard(
        ["2", "AKIATESTEXAMPLE", "sa-east-1", "s", "s", "1"],  # chaves, regiao, confirma, tudo, nao salvar
        secrets=["SEGREDO-SUPER-SECRETO", ""],
        session_factory=fake_session,
        identity_fn=lambda s: {"Account": "111122223333", "Arn": "arn:aws:iam::111122223333:user/x"},
        scan_fn=lambda session, region, services: run_demo(),
    )
    assert wiz.run() == 0
    text = "\n".join(lines)
    assert created["access_key"] == "AKIATESTEXAMPLE"
    assert created["secret_key"] == "SEGREDO-SUPER-SECRETO"
    assert created["region"] == "sa-east-1"
    assert "111122223333" in text
    assert "SEGREDO-SUPER-SECRETO" not in text


def test_declining_account_does_not_scan():
    def boom(*a):
        raise AssertionError("nao deveria escanear")

    wiz, lines = make_wizard(
        ["3", "", "n"],  # credenciais padrao, regiao padrao, nao e essa conta
        session_factory=lambda **kw: object(),
        identity_fn=lambda s: {"Account": "999", "Arn": "arn:x"},
        scan_fn=boom,
    )
    assert wiz.run() == 0
    assert "Nada foi escaneado" in "\n".join(lines)


def test_select_some_services_and_save_json(tmp_path):
    seen = {}
    target = tmp_path / "rel.json"

    def fake_scan(session, region, services):
        seen["services"] = services
        return run_demo()

    wiz, _ = make_wizard(
        ["3", "", "s", "n", "1,3", "2", str(target)],
        session_factory=lambda **kw: object(),
        identity_fn=lambda s: {"Account": "1", "Arn": "a"},
        scan_fn=fake_scan,
    )
    assert wiz.run() == 0
    assert seen["services"] == ["s3", "iam"]
    assert target.exists() and '"findings"' in target.read_text(encoding="utf-8")


def test_ctrl_d_cancels_cleanly():
    def eof(prompt):
        raise EOFError

    lines = []
    wiz = Wizard(input_fn=eof, out=lines.append, color=False)
    assert wiz.run() == 130
    assert any("Cancelado" in line for line in lines)


def test_no_profiles_goes_back_to_menu():
    wiz, lines = make_wizard(["1", "4"], profiles_fn=lambda: [])
    assert wiz.run() == 0
    assert any("Nenhum perfil" in line for line in lines)
