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