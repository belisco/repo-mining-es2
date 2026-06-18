"""Módulo para cálculo de métricas de saúde do repositório."""

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