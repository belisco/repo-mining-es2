"""Módulo para geração de relatórios de métricas do repositório."""

import json
from typing import List, Tuple

import click


class ReportGenerator:
    """Classe responsável por formatar e gerar relatórios de métricas."""

    @staticmethod
    def format_hotspots(hotspots: List[Tuple[str, int]]) -> str:
        if not hotspots:
            return "HOTSPOTS\nNenhum arquivo encontrado"

        report = [click.style("HOTSPOTS", bold=True, fg="cyan")]

        for file, count in hotspots:
            if count >= 10:
                color = "red"
            elif count >= 5:
                color = "yellow"
            else:
                color = "green"
            report.append(f"{click.style(file, fg=color)}: {count} commits")

        return "\n".join(report)

    @staticmethod
    def format_hotspots_json(hotspots: List[Tuple[str, int]]) -> str:
        data = [{"file": file, "commits": count} for file, count in hotspots]
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def format_ownership(ownership: List[Tuple[str, int]]) -> str:
        if not ownership:
            return "OWNERSHIP\nNenhum arquivo encontrado"

        report = [click.style("OWNERSHIP", bold=True, fg="cyan")]

        for file, count in ownership:
            if count >= 5:
                color = "red"
            elif count >= 3:
                color = "yellow"
            else:
                color = "green"
            report.append(f"{click.style(file, fg=color)}: {count} autores")

        return "\n".join(report)

    @staticmethod
    def format_ownership_json(ownership: List[Tuple[str, int]]) -> str:
        data = [{"file": file, "authors": count} for file, count in ownership]
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def format_abandoned(abandoned: List[Tuple[str, int]]) -> str:
        if not abandoned:
            return "ABANDONED FILES\nNenhum arquivo encontrado"

        report = [click.style("ABANDONED FILES", bold=True, fg="cyan")]

        for file, days in abandoned:
            if days >= 365:
                color = "red"
            elif days >= 90:
                color = "yellow"
            else:
                color = "green"
            report.append(f"{click.style(file, fg=color)}: {days} dias sem modificação")

        return "\n".join(report)

    @staticmethod
    def format_abandoned_json(abandoned: List[Tuple[str, int]]) -> str:
        data = [{"file": file, "days_since_modification": days} for file, days in abandoned]
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def format_risk_score(
    risk_scores: List[Tuple[str, int, int, int]]
    ) -> str:
        if not risk_scores:
            return "RISK SCORE\nNenhum arquivo encontrado"

        report = [click.style("RISK SCORE", bold=True, fg="cyan")]

        for file, commits, authors, score in risk_scores:
            if score >= 50:
                color = "red"
            elif score >= 10:
                color = "yellow"
            else:
                color = "green"
            report.append(
                f"{click.style(file, fg=color)}: Score: {score} "
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

    @staticmethod
    def format_bus_factor(bus_factor_results: List[Tuple[str, int, str, float, int]]) -> str:
        if not bus_factor_results:
            return "BUS FACTOR\nNenhum arquivo encontrado"

        report = [click.style("BUS FACTOR", bold=True, fg="cyan")]

        for file, factor, author, percentage, total in bus_factor_results:
            if factor == 1:
                color = "red"
            elif factor == 2:
                color = "yellow"
            else:
                color = "green"

            report.append(
                f"{click.style(file, fg=color)}: Bus Factor: {factor} "
                f"(Principal: {author} ({percentage:.1f}%), Total: {total} commits)"
            )

        return "\n".join(report)

    @staticmethod
    def format_bus_factor_json(bus_factor_results: List[Tuple[str, int, str, float, int]]) -> str:
        data = [
            {
                "file": file,
                "bus_factor": factor,
                "main_author": author,
                "main_author_percentage": round(percentage, 2),
                "total_commits": total
            }
            for file, factor, author, percentage, total in bus_factor_results
        ]
        return json.dumps(data, indent=2, ensure_ascii=False)


