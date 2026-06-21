"""Módulo para cálculo de métricas de saúde do repositório."""

from datetime import datetime
from typing import List, Tuple

from .git_analyzer import GitAnalyzer


class MetricsCalculator:
    """Classe responsável por calcular métricas do repositório."""

    def __init__(self, analyzer: GitAnalyzer):
        """
        Inicializa o calculador de métricas.

        Args:
            analyzer: Instância do GitAnalyzer
        """
        self.analyzer = analyzer

    def calculate_hotspots(
        self,
        top_n: int = 10,
    ) -> List[Tuple[str, int]]:
        """
        Calcula os arquivos mais modificados (hotspots).

        Args:
            top_n: Número de resultados

        Returns:
            Lista de tuplas (arquivo, commits)
        """
        file_commits = self.analyzer.get_file_commit_count()

        sorted_files = sorted(
            file_commits.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return sorted_files[:top_n]

    def calculate_ownership(self) -> List[Tuple[str, int]]:
        """
        Calcula a quantidade de autores por arquivo.

        Returns:
            Lista de tuplas (arquivo, quantidade_autores)
        """
        file_authors = self.analyzer.get_file_authors()

        file_author_count = [
            (file, len(authors))
            for file, authors in file_authors.items()
        ]

        return sorted(
            file_author_count,
            key=lambda x: x[1],
            reverse=True,
        )

    def calculate_abandoned(
        self,
        top_n: int = 10,
    ) -> List[Tuple[str, int]]:
        """
        Calcula os arquivos abandonados (há mais tempo sem modificação).

        Args:
            top_n: Número de resultados

        Returns:
            Lista de tuplas (arquivo, dias_desde_ultima_mod)
        """
        last_modifications = (
            self.analyzer.get_file_last_modification()
        )

        now = datetime.now()

        abandoned_files = []

        for file, last_mod in last_modifications.items():
            days = (now - last_mod).days
            abandoned_files.append((file, days))

        return sorted(
            abandoned_files,
            key=lambda x: x[1],
            reverse=True,
        )[:top_n]

    def calculate_risk_score(
        self,
    ) -> List[Tuple[str, int, int, int]]:
        """
        Calcula o score de risco dos arquivos.

        Returns:
            Lista de tuplas:
            (arquivo, commits, autores, score)
        """
        file_commits = (
            self.analyzer.get_file_commit_count()
        )

        file_authors = (
            self.analyzer.get_file_authors()
        )

        risk_scores = []

        all_files = (
            set(file_commits.keys())
            | set(file_authors.keys())
        )

        for file in all_files:
            commits = file_commits.get(file, 0)

            authors = len(
                file_authors.get(file, set())
            )

            score = commits * authors

            risk_scores.append(
                (
                    file,
                    commits,
                    authors,
                    score,
                )
            )

        return sorted(
            risk_scores,
            key=lambda x: x[3],
            reverse=True,
        )
