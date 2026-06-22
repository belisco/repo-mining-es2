#!/usr/bin/env python3
"""
Script de exemplo para usar o RepoHealth como biblioteca Python.
Este script executa análises programáticas em um repositório Git.
"""

import sys
from pathlib import Path

# Adiciona o diretório pai ao path caso o repohealth não esteja instalado
sys.path.insert(0, str(Path(__file__).parent.parent))

from repohealth.git_analyzer import GitAnalyzer
from repohealth.metrics import MetricsCalculator
from repohealth.reports import ReportGenerator


def main():
    # Define o repositório a ser analisado (o próprio repositório por padrão)
    repo_path = "."
    print(f"Iniciando análise do repositório: {repo_path}\n")

    # Inicializa o analisador e o calculador
    # Exclui arquivos de teste e ambientes virtuais da análise
    analyzer = GitAnalyzer(repo_path, exclude_patterns=["venv/*", "htmlcov/*", ".pytest_cache/*"])
    calculator = MetricsCalculator(analyzer)

    # 1. Hotspots
    print("--- 1. Hotspots (Arquivos mais alterados) ---")
    hotspots = calculator.calculate_hotspots(top_n=5)
    print(ReportGenerator.format_hotspots(hotspots))
    print()

    # 2. Ownership (Gargalo de Autores)
    print("--- 2. Ownership (Número de autores por arquivo) ---")
    ownership = calculator.calculate_ownership(top_n=5)
    print(ReportGenerator.format_ownership(ownership))
    print()

    # 3. Bus Factor (Fator de Gargalo)
    print("--- 3. Bus Factor (Dependência de desenvolvedores) ---")
    bus_factor = calculator.calculate_bus_factor(top_n=5)
    print(ReportGenerator.format_bus_factor(bus_factor))
    print()


if __name__ == "__main__":
    main()
