"""Módulo para geração de relatórios de métricas do repositório."""

import json
from typing import List, Tuple


class ReportGenerator:
    """Classe responsável por formatar e gerar relatórios de métricas."""

    @staticmethod
    def format_hotspots(hotspots: List[Tuple[str, int]]) -> str:
        if not hotspots:
            return "HOTSPOTS\nNenhum arquivo encontrado"

        report = ["HOTSPOTS"]

        for file, count in hotspots:
            report.append(f"{file}: {count} commits")

        return "\n".join(report)

    @staticmethod
    def format_hotspots_json(hotspots: List[Tuple[str, int]]) -> str:
        data = [{"file": file, "commits": count} for file, count in hotspots]
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def format_ownership(ownership: List[Tuple[str, int]]) -> str:
        report = ["OWNERSHIP"]

        for file, count in ownership:
            report.append(f"{file}: {count} autores")

        return "\n".join(report)

    @staticmethod
    def format_ownership_json(ownership: List[Tuple[str, int]]) -> str:
        data = [{"file": file, "authors": count} for file, count in ownership]
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def format_abandoned(abandoned: List[Tuple[str, int]]) -> str:
        report = ["ABANDONED FILES"]

        for file, days in abandoned:
            report.append(f"{file}: {days} dias sem modificação")

        return "\n".join(report)

    @staticmethod
    def format_abandoned_json(abandoned: List[Tuple[str, int]]) -> str:
        data = [{"file": file, "days_since_modification": days} for file, days in abandoned]
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def format_risk_score(
    risk_scores: List[Tuple[str, int, int, int]]
    ) -> str:
        report = ["RISK SCORE"]

        for file, commits, authors, score in risk_scores:
            report.append(
                f"{file}: Score: {score} "
                f"(commits={commits}, autores={authors})"
            )

        return "\n".join(report)

    @staticmethod
    def format_risk_score_json(
        risk_scores: List[Tuple[str, int, int, int]]
    ) -> str:
        data = [
            {"file": file, "commits": commits, "authors": authors, "risk_score": score}
            for file, commits, authors, score in risk_scores
        ]
        return json.dumps(data, indent=2, ensure_ascii=False)


