"""Módulo para cálculo de métricas de saúde do repositório."""

from .git_analyzer import GitAnalyzer

from typing import List, Tuple

class MetricsCalculator:
    """Classe responsável por calcular métricas do repositório."""

    def __init__(self, analyzer: GitAnalyzer):
        """
        Inicializa o calculador de métricas.

        Args:
            analyzer: Instância do GitAnalyzer
        """
        self.analyzer = analyzer

    def calculate_hotspots(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Calcula os arquivos mais modificados (hotspots).

        Args:
            top_n: Número de resultados

        Returns:
            Lista de tuplas (arquivo, commits)
        """
        file_commits = self.analyzer.get_file_commit_count()
        sorted_files = sorted(file_commits.items(), key=lambda x: x[1], reverse=True)
        return sorted_files[:top_n]

    def calculate_ownership(self) -> List[Tuple[str, int]]:
        """
        Calcula a quantidade de autores por arquivo.

        Returns:
            Lista de tuplas (arquivo, quantidade_autores)
        """
        file_authors = self.analyzer.get_file_authors()
        file_author_count = [(file, len(authors)) for file, authors in file_authors.items()]
        return sorted(file_author_count, key=lambda x: x[1], reverse=True)