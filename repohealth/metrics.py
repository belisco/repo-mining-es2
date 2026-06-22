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

    def calculate_ownership(
        self,
        top_n: int = None,
    ) -> List[Tuple[str, int]]:
        """
        Calcula a quantidade de autores por arquivo.

        Args:
            top_n: Número de resultados a retornar

        Returns:
            Lista de tuplas (arquivo, quantidade_autores)
        """
        file_authors = self.analyzer.get_file_authors()

        file_author_count = [
            (file, len(authors))
            for file, authors in file_authors.items()
        ]

        sorted_files = sorted(
            file_author_count,
            key=lambda x: x[1],
            reverse=True,
        )

        if top_n is not None:
            return sorted_files[:top_n]
        return sorted_files

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
        top_n: int = None,
    ) -> List[Tuple[str, int, int, int]]:
        """
        Calcula o score de risco dos arquivos.

        Args:
            top_n: Número de resultados a retornar

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

        sorted_files = sorted(
            risk_scores,
            key=lambda x: x[3],
            reverse=True,
        )

        if top_n is not None:
            return sorted_files[:top_n]
        return sorted_files

    def calculate_bus_factor(
        self,
        top_n: int = None,
    ) -> List[Tuple[str, int, str, float, int]]:
        """
        Calcula o Bus Factor por arquivo.

        Bus Factor é o número mínimo de desenvolvedores necessários para atingir
        mais de 50% dos commits do arquivo.

        Args:
            top_n: Número de resultados a retornar

        Returns:
            Lista de tuplas (arquivo, bus_factor, autor_principal, percentual_autor_principal, total_commits)
        """
        file_author_commits = self.analyzer.get_file_author_commits()
        bus_factors = []

        for file, author_counts in file_author_commits.items():
            total_commits = sum(author_counts.values())
            if total_commits == 0:
                continue

            # Ordena autores por número de commits de forma decrescente
            sorted_authors = sorted(
                author_counts.items(),
                key=lambda x: x[1],
                reverse=True,
            )

            # Calcula o bus factor
            bus_factor = 0
            cumulative_commits = 0
            half_commits = total_commits / 2.0

            for author, count in sorted_authors:
                cumulative_commits += count
                bus_factor += 1
                if cumulative_commits > half_commits:
                    break

            main_author, main_commits = sorted_authors[0]
            main_percentage = (main_commits / total_commits) * 100.0

            bus_factors.append(
                (
                    file,
                    bus_factor,
                    main_author,
                    main_percentage,
                    total_commits,
                )
            )

        # Ordenação: menor bus factor (mais risco), depois maior número total de commits (mais criticidade)
        sorted_files = sorted(
            bus_factors,
            key=lambda x: (x[1], -x[4]),
        )

        if top_n is not None:
            return sorted_files[:top_n]
        return sorted_files
