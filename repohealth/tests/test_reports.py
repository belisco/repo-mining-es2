"""Testes para o módulo reports."""

from repohealth.reports import ReportGenerator


def test_format_hotspots_empty():
    """Testa formatação de hotspots vazio."""
    result = ReportGenerator.format_hotspots([])
    assert "Nenhum arquivo encontrado" in result


def test_format_hotspots_with_data():
    """Testa formatação de hotspots com dados."""
    data = [("file_a.py", 10), ("file_b.py", 5)]
    result = ReportGenerator.format_hotspots(data)
    
    assert "HOTSPOTS" in result
    assert "file_a.py" in result
    assert "10" in result


def test_format_ownership_with_data():
    """Testa formatação de ownership."""
    data = [("file_a.py", 3), ("file_b.py", 1)]
    result = ReportGenerator.format_ownership(data)
    
    assert "OWNERSHIP" in result
    assert "file_a.py" in result


def test_format_risk_score_with_data():
    """Testa formatação de risk score."""
    data = [("file_a.py", 10, 3, 30)]
    result = ReportGenerator.format_risk_score(data)
    
    assert "RISK SCORE" in result
    assert "Score: 30" in result


def test_format_abandoned_with_data():
    """Testa formatação de abandoned files."""
    data = [("file_a.py", 45)]
    result = ReportGenerator.format_abandoned(data)
    
    assert "ABANDONED FILES" in result
    assert "file_a.py" in result
    assert "45 dias sem modificação" in result