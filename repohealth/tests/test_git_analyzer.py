"""Testes para o módulo git_analyzer."""
import gc
import shutil
import tempfile
from pathlib import Path

import pytest
from git import Repo

from repohealth.git_analyzer import GitAnalyzer


@pytest.fixture
def temp_repo():
    """Cria um repositório Git temporário para testes."""
    tmpdir = tempfile.mkdtemp()
    repo = Repo.init(tmpdir)

    with repo.config_writer() as config:
        config.set_value("user", "name", "Test User")
        config.set_value("user", "email", "test@example.com")

    test_file = Path(tmpdir) / "test.txt"
    test_file.write_text("Initial content")
    repo.index.add(["test.txt"])
    repo.index.commit("Initial commit")

    test_file.write_text("Modified content")
    repo.index.add(["test.txt"])
    repo.index.commit("Modify test.txt")

    yield tmpdir

    repo.close()
    gc.collect()
    shutil.rmtree(tmpdir, ignore_errors=True)

def test_git_analyzer_initialization(temp_repo):
    """Testa a inicialização do GitAnalyzer."""
    analyzer = GitAnalyzer(temp_repo)
    assert analyzer.repo_path == Path(temp_repo)
    assert analyzer.repo is not None


def test_get_all_commits(temp_repo):
    """Testa a recuperação de todos os commits."""
    analyzer = GitAnalyzer(temp_repo)
    commits = analyzer.get_all_commits()
    assert len(commits) == 2


def test_get_file_commit_count(temp_repo):
    """Testa a contagem de commits por arquivo."""
    analyzer = GitAnalyzer(temp_repo)
    file_commits = analyzer.get_file_commit_count()
    
    assert "test.txt" in file_commits
    assert file_commits["test.txt"] == 2


def test_get_file_authors(temp_repo):
    """Testa a identificação de autores por arquivo."""
    analyzer = GitAnalyzer(temp_repo)
    file_authors = analyzer.get_file_authors()
    
    assert "test.txt" in file_authors
    assert "test@example.com" in file_authors["test.txt"]

def test_get_file_last_modification(temp_repo):
    """Testa recuperação de última modificação."""
    analyzer = GitAnalyzer(temp_repo)
    file_last_mod = analyzer.get_file_last_modification()
    
    assert "test.txt" in file_last_mod
    assert file_last_mod["test.txt"] is not None


def test_get_all_tracked_files(temp_repo):
    """Testa a listagem de arquivos rastreados."""
    analyzer = GitAnalyzer(temp_repo)
    tracked = analyzer.get_all_tracked_files()
    assert "test.txt" in tracked


def test_git_analyzer_empty_repo():
    """Testa o comportamento do GitAnalyzer em um repositório sem commits ou inválido."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Repo.init(tmpdir)
        analyzer = GitAnalyzer(tmpdir)
        
        # Repositório inicializado mas sem commits
        assert analyzer.get_all_commits() == []
        assert analyzer.get_file_commit_count() == {}
        assert analyzer.get_file_authors() == {}
        assert analyzer.get_file_last_modification() == {}
        assert analyzer.get_file_author_commits() == {}
        
        repo.close()


def test_git_analyzer_exclude(temp_repo):
    """Testa a exclusão de arquivos com padrões glob/diretório."""
    analyzer = GitAnalyzer(temp_repo, exclude_patterns=["*.txt", "ignored_dir/"])
    
    # test.txt deve ser filtrado
    assert "test.txt" not in analyzer.get_file_commit_count()
    assert "test.txt" not in analyzer.get_file_authors()
    assert "test.txt" not in analyzer.get_file_last_modification()
    assert "test.txt" not in analyzer.get_all_tracked_files()


def test_get_file_author_commits(temp_repo):
    """Testa a obtenção do número de commits por autor por arquivo."""
    analyzer = GitAnalyzer(temp_repo)
    author_commits = analyzer.get_file_author_commits()
    
    assert "test.txt" in author_commits
    assert "test@example.com" in author_commits["test.txt"]
    assert author_commits["test.txt"]["test@example.com"] == 2
