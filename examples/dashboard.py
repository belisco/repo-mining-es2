#!/usr/bin/env python3
"""
Script de exemplo para gerar um Dashboard HTML interativo dos dados do RepoHealth.
Executa a análise e cria um arquivo 'dashboard.html' com gráficos.
"""

import json
import sys
from pathlib import Path

# Adiciona o diretório pai ao path caso o repohealth não esteja instalado
sys.path.insert(0, str(Path(__file__).parent.parent))

from repohealth.git_analyzer import GitAnalyzer
from repohealth.metrics import MetricsCalculator


def main():
    repo_path = "."
    print(f"Gerando dados do dashboard para o repositório: {repo_path}...")

    # Analisa o repositório
    analyzer = GitAnalyzer(repo_path, exclude_patterns=["venv/*", "htmlcov/*", ".pytest_cache/*"])
    calculator = MetricsCalculator(analyzer)

    # Coleta os dados em formato JSON
    hotspots = [
        {"file": f, "commits": c}
        for f, c in calculator.calculate_hotspots(top_n=8)
    ]
    
    risk_scores = [
        {"file": f, "commits": c, "authors": a, "risk_score": r}
        for f, c, a, r in calculator.calculate_risk_score(top_n=8)
    ]

    bus_factors = [
        {"file": f, "bus_factor": b, "main_author": a, "main_author_percentage": round(p, 1), "total_commits": tc}
        for f, b, a, p, tc in calculator.calculate_bus_factor(top_n=8)
    ]

    # Conteúdo do HTML Dashboard
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RepoHealth - Dashboard</title>
    <!-- Tailwind CSS para estilização moderna -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js para renderização de gráficos -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
        }}
    </style>
</head>
<body class="p-6 md:p-12">
    <div class="max-w-7xl mx-auto space-y-8">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-800 pb-6">
            <div>
                <h1 class="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                    RepoHealth Dashboard
                </h1>
                <p class="text-slate-400 mt-2">Relatório de Saúde de Repositório Git</p>
            </div>
            <div class="mt-4 md:mt-0 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-300">
                Analisado: <span class="font-semibold text-white">{repo_path}</span>
            </div>
        </div>

        <!-- Cards de Métricas Principais -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Card 1 -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-2">
                <span class="text-xs font-semibold tracking-wider text-cyan-400 uppercase">Principal Hotspot</span>
                <h3 class="text-lg font-bold truncate text-slate-100" id="top-hotspot-file">-</h3>
                <p class="text-slate-400 text-sm"><span class="text-white font-semibold" id="top-hotspot-val">0</span> commits</p>
            </div>
            <!-- Card 2 -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-2">
                <span class="text-xs font-semibold tracking-wider text-rose-400 uppercase">Arquivo de Maior Risco</span>
                <h3 class="text-lg font-bold truncate text-slate-100" id="top-risk-file">-</h3>
                <p class="text-slate-400 text-sm">Score: <span class="text-white font-semibold" id="top-risk-val">0</span></p>
            </div>
            <!-- Card 3 -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-2">
                <span class="text-xs font-semibold tracking-wider text-amber-400 uppercase">Maior Dependência (Bus Factor 1)</span>
                <h3 class="text-lg font-bold truncate text-slate-100" id="top-bf-file">-</h3>
                <p class="text-slate-400 text-sm">Responsável: <span class="text-white font-semibold" id="top-bf-author">-</span></p>
            </div>
        </div>

        <!-- Gráficos -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Gráfico Hotspots -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h2 class="text-xl font-bold mb-4 text-slate-100">Hotspots (Commits por Arquivo)</h2>
                <div class="h-80">
                    <canvas id="hotspotsChart"></canvas>
                </div>
            </div>
            <!-- Gráfico Risk Score -->
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h2 class="text-xl font-bold mb-4 text-slate-100">Score de Risco (Commits × Autores)</h2>
                <div class="h-80">
                    <canvas id="riskChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Tabela Bus Factor -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h2 class="text-xl font-bold mb-4 text-slate-100">Fator de Gargalo (Bus Factor por Arquivo)</h2>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-slate-800">
                    <thead>
                        <tr class="text-slate-400 text-left text-xs uppercase tracking-wider">
                            <th class="py-3 px-4">Arquivo</th>
                            <th class="py-3 px-4 text-center">Bus Factor</th>
                            <th class="py-3 px-4">Autor Principal</th>
                            <th class="py-3 px-4 text-right">Participação</th>
                            <th class="py-3 px-4 text-right">Commits Totais</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800 text-sm" id="bus-factor-table">
                        <!-- Inserido dinamicamente -->
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <!-- Script de Configuração dos Dados -->
    <script>
        // Dados injetados pelo Python
        const hotspotsData = {json.dumps(hotspots)};
        const riskData = {json.dumps(risk_scores)};
        const busFactorData = {json.dumps(bus_factors)};

        // Preenche os cards
        if (hotspotsData.length > 0) {{
            document.getElementById('top-hotspot-file').innerText = hotspotsData[0].file;
            document.getElementById('top-hotspot-file').title = hotspotsData[0].file;
            document.getElementById('top-hotspot-val').innerText = hotspotsData[0].commits;
        }}
        if (riskData.length > 0) {{
            document.getElementById('top-risk-file').innerText = riskData[0].file;
            document.getElementById('top-risk-file').title = riskData[0].file;
            document.getElementById('top-risk-val').innerText = riskData[0].risk_score;
        }}
        if (busFactorData.length > 0) {{
            const bf1 = busFactorData.find(item => item.bus_factor === 1);
            if (bf1) {{
                document.getElementById('top-bf-file').innerText = bf1.file;
                document.getElementById('top-bf-file').title = bf1.file;
                document.getElementById('top-bf-author').innerText = bf1.main_author + ' (' + bf1.main_author_percentage + '%)';
            }}
        }}

        // Renderiza Gráfico Hotspots
        const ctxHotspots = document.getElementById('hotspotsChart').getContext('2d');
        new Chart(ctxHotspots, {{
            type: 'bar',
            data: {{
                labels: hotspotsData.map(d => d.file.split('/').pop()),
                datasets: [{{
                    label: 'Commits',
                    data: hotspotsData.map(d => d.commits),
                    backgroundColor: 'rgba(34, 211, 238, 0.6)',
                    borderColor: 'rgba(34, 211, 238, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }},
                    x: {{ ticks: {{ color: '#94a3b8' }} }}
                }}
            }}
        }});

        // Renderiza Gráfico Risk Score
        const ctxRisk = document.getElementById('riskChart').getContext('2d');
        new Chart(ctxRisk, {{
            type: 'line',
            data: {{
                labels: riskData.map(d => d.file.split('/').pop()),
                datasets: [{{
                    label: 'Score de Risco',
                    data: riskData.map(d => d.risk_score),
                    backgroundColor: 'rgba(244, 63, 94, 0.2)',
                    borderColor: 'rgba(244, 63, 94, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }},
                    x: {{ ticks: {{ color: '#94a3b8' }} }}
                }}
            }}
        }});

        // Renderiza Tabela Bus Factor
        const tbody = document.getElementById('bus-factor-table');
        busFactorData.forEach(item => {{
            const tr = document.createElement('tr');
            
            // Badge color dependendo do Bus Factor
            let badgeColor = "bg-green-500/10 text-green-400 border border-green-500/20";
            if (item.bus_factor === 1) {{
                badgeColor = "bg-red-500/10 text-red-400 border border-red-500/20";
            }} else if (item.bus_factor === 2) {{
                badgeColor = "bg-amber-500/10 text-amber-400 border border-amber-500/20";
            }}

            tr.innerHTML = `
                <td class="py-3 px-4 font-medium text-slate-300 truncate max-w-xs" title="${{item.file}}">${{item.file}}</td>
                <td class="py-3 px-4 text-center">
                    <span class="px-2 py-1 rounded-full text-xs font-semibold ${{badgeColor}}">
                        ${{item.bus_factor}}
                    </span>
                </td>
                <td class="py-3 px-4 text-slate-400">${{item.main_author}}</td>
                <td class="py-3 px-4 text-right font-medium text-slate-300">${{item.main_author_percentage}}%</td>
                <td class="py-3 px-4 text-right text-slate-400">${{item.total_commits}}</td>
            `;
            tbody.appendChild(tr);
        }});
    </script>
</body>
</html>
"""

    # Escreve o dashboard.html na pasta atual
    output_path = Path("dashboard.html")
    output_path.write_text(html_content, encoding="utf-8")
    print(f"Sucesso! O painel interativo foi salvo em: {output_path.absolute()}")
    print("Você pode abrir este arquivo diretamente em qualquer navegador web para ver os gráficos!")


if __name__ == "__main__":
    main()
