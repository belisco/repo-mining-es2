import tempfile
from pathlib import Path

import pytest
from git import Repo

from repohealth.git_analyzer import GitAnalyzer


@pytest.fixture
def temp_repo():
    """Cria um repositório Git temporário para testes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Repo.init(tmpdir)
        
        # Configura o autor
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")
        
        # Cria arquivo e commit
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("Initial content")
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")
        
        # Modifica arquivo
        test_file.write_text("Modified content")
        repo.index.add(["test.txt"])
        repo.index.commit("Modify test.txt")
        
        yield tmpdir
