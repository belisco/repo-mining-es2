"""Testes para o módulo CLI."""

import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner
from git import Repo

from repohealth.cli import cli


@pytest.fixture
def temp_repo_cli():
    """Cria repositório para testar CLI."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Repo.init(tmpdir)
        
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test")
            config.set_value("user", "email", "test@test.com")
        
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("print('hello')")
        repo.index.add(["test.py"])
        repo.index.commit("Initial")
        
        yield tmpdir


def test_cli_hotspots_command(temp_repo_cli):
    """Testa comando hotspots."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--repo", temp_repo_cli, "hotspots"])
    
    assert result.exit_code == 0
    assert "HOTSPOTS" in result.output


def test_cli_invalid_repo():
    """Testa erro com repositório inválido."""
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, ["--repo", tmpdir, "hotspots"])
        
        assert result.exit_code == 1
        assert "não é um repositório Git válido" in result.output