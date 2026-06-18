"""Módulo para geração de relatórios de métricas do repositório."""

from typing import List, Tuple, Dict

class ReportGenerator:
    """Classe responsável por formatar e gerar relatórios de métricas."""

    @staticmethod
    def format_hotspots(hotspots: List[Tuple[str, int]]) -> str:
        """
        Formata o relatório de hotspots.

        Args:
            hotspots: Lista de tuplas (arquivo, número de commits)

        Returns:
            String formatada com o relatório
        """
        report = ["--- Hotspots (Arquivos mais modificados) ---"]
        for file, count in hotspots:
            report.append(f"{file}: {count} commits")
        return "\n".join(report)

    @staticmethod
    def format_ownership(ownership: List[Tuple[str, int]]) -> str:
        """
        Formata o relatório de propriedade de código.

        Args:
            ownership: Lista de tuplas (arquivo, número de autores)

        Returns:
            String formatada com o relatório
        """
        report = ["--- Ownership (Autores por arquivo) ---"]
        for file, count in ownership:
            report.append(f"{file}: {count} autores")
        return "\n".join(report)

    @staticmethod
    def format_abandoned(abandoned: List[Tuple[str, int]]) -> str:
        """
        Formata o relatório de arquivos abandonados.

        Args:
            abandoned: Lista de tuplas (arquivo, dias_desde_ultima_mod)

        Returns:
            String formatada com o relatório
        """
        report = ["--- Arquivos Abandonados ---"]
        for file, days in abandoned:
            report.append(f"{file}: {days} dias sem modificação")
        return "\n".join(report)

    @staticmethod
    def format_risk_score(risk_scores: List[Dict]) -> str:
        """
        Formata o relatório de score de risco.

        Args:
            risk_scores: Lista de dicionários contendo as métricas e o score

        Returns:
            String formatada com o relatório
        """
        report = ["--- Risk Score (Commits × Autores) ---"]

        for item in risk_scores:
            report.append(
                f"{item['file']}: "
                f"{item['risk_score']} "
                f"(commits={item['commits']}, autores={item['authors']})"
            )

        return "\n".join(report)
