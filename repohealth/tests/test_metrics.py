"""Testes para o módulo metrics."""
import gc
import shutil
import tempfile
from pathlib import Path

import pytest
from git import Repo

from repohealth.git_analyzer import GitAnalyzer
from repohealth.metrics import MetricsCalculator


@pytest.fixture
def temp_repo_metrics():
    """Cria repositório para testar métricas."""
    tmpdir = tempfile.mkdtemp()
    repo = Repo.init(tmpdir)

    with repo.config_writer() as config:
        config.set_value("user", "name", "Dev One")
        config.set_value("user", "email", "dev1@example.com")

    file_a = Path(tmpdir) / "file_a.py"
    file_a.write_text("def func(): pass")
    repo.index.add(["file_a.py"])
    repo.index.commit("Add file_a")

    file_a.write_text("def func(): return 1")
    repo.index.add(["file_a.py"])
    repo.index.commit("Modify file_a")

    file_b = Path(tmpdir) / "file_b.py"
    file_b.write_text("def other(): pass")
    repo.index.add(["file_b.py"])
    repo.index.commit("Add file_b")

    yield tmpdir

    repo.close()
    gc.collect()
    shutil.rmtree(tmpdir, ignore_errors=True)


def test_calculate_hotspots(temp_repo_metrics):
    """Testa o cálculo de hotspots."""
    analyzer = GitAnalyzer(temp_repo_metrics)
    calculator = MetricsCalculator(analyzer)
    
    hotspots = calculator.calculate_hotspots(top_n=10)
    
    assert len(hotspots) > 0
    # file_a deve ter mais commits
    assert hotspots[0][0] == "file_a.py"


def test_calculate_ownership(temp_repo_metrics):
    """Testa o cálculo de ownership."""
    analyzer = GitAnalyzer(temp_repo_metrics)
    calculator = MetricsCalculator(analyzer)
    
    ownership = calculator.calculate_ownership()
    
    assert len(ownership) > 0


def test_calculate_risk_score(temp_repo_metrics):
    """Testa o cálculo de score de risco."""
    analyzer = GitAnalyzer(temp_repo_metrics)
    calculator = MetricsCalculator(analyzer)
    
    risk_scores = calculator.calculate_risk_score()
    
    assert len(risk_scores) > 0
    for file, commits, authors, score in risk_scores:
        assert score == commits * authors

def test_calculate_abandoned(temp_repo_metrics):
    """Testa cálculo de arquivos abandonados."""
    analyzer = GitAnalyzer(temp_repo_metrics)
    calculator = MetricsCalculator(analyzer)
    
    abandoned = calculator.calculate_abandoned(top_n=10)
    
    assert len(abandoned) > 0
    for file, days in abandoned:
        assert days >= 0
