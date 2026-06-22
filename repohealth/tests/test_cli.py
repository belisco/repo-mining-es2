"""Testes para o módulo CLI."""

import gc
import shutil
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner
from git import Repo

from repohealth.cli import cli


@pytest.fixture
def temp_repo_cli():
    """Cria repositório para testar CLI."""
    tmpdir = tempfile.mkdtemp()
    repo = Repo.init(tmpdir)

    with repo.config_writer() as config:
        config.set_value("user", "name", "Test")
        config.set_value("user", "email", "test@test.com")

    test_file = Path(tmpdir) / "test.py"
    test_file.write_text("print('hello')")
    repo.index.add(["test.py"])
    repo.index.commit("Initial")

    yield tmpdir

    repo.close()
    gc.collect()
    shutil.rmtree(tmpdir, ignore_errors=True)


def test_cli_hotspots_command(temp_repo_cli):
    """Testa comando hotspots."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--repo", temp_repo_cli, "hotspots"])
    
    assert result.exit_code == 0
    assert "HOTSPOTS" in result.output


def test_cli_ownership_command(temp_repo_cli):
    """Testa comando ownership."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--repo", temp_repo_cli, "ownership"])
    
    assert result.exit_code == 0
    assert "OWNERSHIP" in result.output


def test_cli_abandoned_command(temp_repo_cli):
    """Testa comando abandoned."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--repo", temp_repo_cli, "abandoned"])
    
    assert result.exit_code == 0
    assert "ABANDONED" in result.output


def test_cli_risk_command(temp_repo_cli):
    """Testa comando risk."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--repo", temp_repo_cli, "risk"])
    
    assert result.exit_code == 0
    assert "RISK SCORE" in result.output


def test_cli_invalid_repo():
    """Testa erro com repositório inválido."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, ["--repo", tmpdir, "hotspots"])
        
        assert result.exit_code == 1
        assert "não é um repositório Git válido" in result.output


def test_cli_main(monkeypatch):
    """Testa a função main do CLI."""
    from repohealth.cli import main
    # Mock cli call to prevent actual execution but ensure it's called
    called = False
    def mock_cli(*args, **kwargs):
        nonlocal called
        called = True
    monkeypatch.setattr("repohealth.cli.cli", mock_cli)
    main()
    assert called


def test_cli_json_format(temp_repo_cli):
    """Testa a saída em formato JSON de todos os comandos do CLI."""
    import json
    runner = CliRunner()
    
    # hotspots json
    res = runner.invoke(cli, ["--repo", temp_repo_cli, "--format", "json", "hotspots"])
    assert res.exit_code == 0
    data = json.loads(res.output)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "file" in data[0]
    assert "commits" in data[0]
    
    # ownership json
    res = runner.invoke(cli, ["--repo", temp_repo_cli, "--format", "json", "ownership"])
    assert res.exit_code == 0
    data = json.loads(res.output)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "file" in data[0]
    assert "authors" in data[0]
    
    # abandoned json
    res = runner.invoke(cli, ["--repo", temp_repo_cli, "--format", "json", "abandoned"])
    assert res.exit_code == 0
    data = json.loads(res.output)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "file" in data[0]
    assert "days_since_modification" in data[0]
    
    # risk json
    res = runner.invoke(cli, ["--repo", temp_repo_cli, "--format", "json", "risk"])
    assert res.exit_code == 0
    data = json.loads(res.output)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "file" in data[0]
    assert "risk_score" in data[0]


def test_cli_exclude_option(temp_repo_cli):
    """Testa se a opção --exclude filtra corretamente os arquivos no CLI."""
    runner = CliRunner()
    
    # Executa hotspots sem exclusão
    res_normal = runner.invoke(cli, ["--repo", temp_repo_cli, "hotspots"])
    assert res_normal.exit_code == 0
    assert "test.py" in res_normal.output
    
    # Executa hotspots com exclusão do arquivo test.py
    res_excluded = runner.invoke(cli, ["--repo", temp_repo_cli, "--exclude", "test.py", "hotspots"])
    assert res_excluded.exit_code == 0
    assert "test.py" not in res_excluded.output


def test_cli_bus_factor_command(temp_repo_cli):
    """Testa o comando bus-factor no CLI."""
    import json
    runner = CliRunner()
    
    # Text output check
    result = runner.invoke(cli, ["--repo", temp_repo_cli, "bus-factor"])
    assert result.exit_code == 0
    assert "BUS FACTOR" in result.output
    assert "test.py" in result.output
    
    # JSON output check
    result_json = runner.invoke(cli, ["--repo", temp_repo_cli, "--format", "json", "bus-factor"])
    assert result_json.exit_code == 0
    data = json.loads(result_json.output)
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["file"] == "test.py"
    assert data[0]["bus_factor"] == 1
    assert "main_author" in data[0]