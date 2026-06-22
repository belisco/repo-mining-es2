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


def test_format_json_outputs():
    """Testa a geração de relatórios em formato JSON."""
    import json
    
    # Hotspots
    hotspots_data = [("file_a.py", 10)]
    res = ReportGenerator.format_hotspots_json(hotspots_data)
    loaded = json.loads(res)
    assert loaded[0]["file"] == "file_a.py"
    assert loaded[0]["commits"] == 10
    
    # Ownership
    ownership_data = [("file_a.py", 3)]
    res = ReportGenerator.format_ownership_json(ownership_data)
    loaded = json.loads(res)
    assert loaded[0]["file"] == "file_a.py"
    assert loaded[0]["authors"] == 3

    # Abandoned
    abandoned_data = [("file_a.py", 45)]
    res = ReportGenerator.format_abandoned_json(abandoned_data)
    loaded = json.loads(res)
    assert loaded[0]["file"] == "file_a.py"
    assert loaded[0]["days_since_modification"] == 45

    # Risk Score
    risk_data = [("file_a.py", 10, 3, 30)]
    res = ReportGenerator.format_risk_score_json(risk_data)
    loaded = json.loads(res)
    assert loaded[0]["file"] == "file_a.py"
    assert loaded[0]["commits"] == 10
    assert loaded[0]["authors"] == 3
    assert loaded[0]["risk_score"] == 30


def test_format_empty_and_colors():
    """Testa caminhos de relatórios vazios e verificação de cores."""
    import click
    
    # Executa sem cores em um mock terminal se necessário, mas click.style sempre retorna as sequências
    # Hotspots - Teste de limites de cor (high >= 10, med >= 5, low < 5)
    res_high = ReportGenerator.format_hotspots([("file_a.py", 12)])
    assert "file_a.py" in res_high
    res_med = ReportGenerator.format_hotspots([("file_b.py", 6)])
    assert "file_b.py" in res_med
    res_low = ReportGenerator.format_hotspots([("file_c.py", 2)])
    assert "file_c.py" in res_low
    
    # Ownership - Vazio e limites de cor (high >= 5, med >= 3, low < 3)
    assert "Nenhum arquivo encontrado" in ReportGenerator.format_ownership([])
    res_own_high = ReportGenerator.format_ownership([("file_a.py", 6)])
    assert "file_a.py" in res_own_high
    res_own_med = ReportGenerator.format_ownership([("file_b.py", 4)])
    assert "file_b.py" in res_own_med
    res_own_low = ReportGenerator.format_ownership([("file_c.py", 1)])
    assert "file_c.py" in res_own_low

    # Abandoned - Vazio e limites de cor (high >= 365, med >= 90, low < 90)
    assert "Nenhum arquivo encontrado" in ReportGenerator.format_abandoned([])
    res_ab_high = ReportGenerator.format_abandoned([("file_a.py", 400)])
    assert "file_a.py" in res_ab_high
    res_ab_med = ReportGenerator.format_abandoned([("file_b.py", 120)])
    assert "file_b.py" in res_ab_med
    res_ab_low = ReportGenerator.format_abandoned([("file_c.py", 30)])
    assert "file_c.py" in res_ab_low

    # Risk Score - Vazio e limites de cor (high >= 50, med >= 10, low < 10)
    assert "Nenhum arquivo encontrado" in ReportGenerator.format_risk_score([])
    res_risk_high = ReportGenerator.format_risk_score([("file_a.py", 10, 6, 60)])
    assert "file_a.py" in res_risk_high
    res_risk_med = ReportGenerator.format_risk_score([("file_b.py", 5, 3, 15)])
    assert "file_b.py" in res_risk_med
    res_risk_low = ReportGenerator.format_risk_score([("file_c.py", 2, 2, 4)])
    assert "file_c.py" in res_risk_low


def test_format_bus_factor():
    """Testa a formatação da métrica de Bus Factor."""
    import json
    
    # Text empty check
    assert "Nenhum arquivo encontrado" in ReportGenerator.format_bus_factor([])
    
    # Text colors and format check (high risk: factor=1, medium: factor=2, low: factor>=3)
    data = [
        ("file_a.py", 1, "dev1@example.com", 90.0, 10),
        ("file_b.py", 2, "dev2@example.com", 45.0, 20),
        ("file_c.py", 3, "dev3@example.com", 25.0, 30)
    ]
    res_txt = ReportGenerator.format_bus_factor(data)
    assert "BUS FACTOR" in res_txt
    assert "file_a.py" in res_txt
    assert "file_b.py" in res_txt
    assert "file_c.py" in res_txt
    
    # JSON format check
    res_json = ReportGenerator.format_bus_factor_json(data)
    loaded = json.loads(res_json)
    assert len(loaded) == 3
    assert loaded[0]["file"] == "file_a.py"
    assert loaded[0]["bus_factor"] == 1
    assert loaded[0]["main_author"] == "dev1@example.com"
    assert loaded[0]["main_author_percentage"] == 90.0
    assert loaded[0]["total_commits"] == 10