"""CLI para a ferramenta RepoHealth."""


from .git_analyzer import GitAnalyzer
from .metrics import MetricsCalculator
from .reports import ReportGenerator
import sys
from pathlib import Path

import click


@click.group()
@click.option("--repo", default=".", help="Caminho para o repositório Git")
@click.option(
    "--format",
    default="text",
    type=click.Choice(["text", "json"]),
    help="Formato de saída (text ou json)",
)
@click.option(
    "--exclude",
    default=None,
    help="Padrões para excluir da análise (separados por vírgula)",
)
@click.pass_context
def cli(ctx, repo, format, exclude):
    """RepoHealth - Ferramenta de análise de saúde de repositórios Git."""
    ctx.ensure_object(dict)
    
    # Valida se é um repositório Git
    repo_path = Path(repo)
    if not (repo_path / ".git").exists():
        click.echo(f"Erro: '{repo}' não é um repositório Git válido.", err=True)
        sys.exit(1)
    
    exclude_patterns = []
    if exclude:
        exclude_patterns = [p.strip() for p in exclude.split(",") if p.strip()]

    # Inicializa analisadores
    ctx.obj["analyzer"] = GitAnalyzer(repo, exclude_patterns=exclude_patterns)
    ctx.obj["calculator"] = MetricsCalculator(ctx.obj["analyzer"])
    ctx.obj["format"] = format


@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def hotspots(ctx, top):
    """Identifica os arquivos mais modificados (hotspots)."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_hotspots(top_n=top)
    if ctx.obj.get("format") == "json":
        report = ReportGenerator.format_hotspots_json(results)
        click.echo(report)
    else:
        report = ReportGenerator.format_hotspots(results)
        click.echo(report, color=True)

@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def ownership(ctx, top):
    """Identifica a quantidade de autores por arquivo."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_ownership(top_n=top)
    if ctx.obj.get("format") == "json":
        report = ReportGenerator.format_ownership_json(results)
        click.echo(report)
    else:
        report = ReportGenerator.format_ownership(results)
        click.echo(report, color=True)
    
@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def abandoned(ctx, top):
    """Mostra arquivos sem modificações há mais tempo."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_abandoned(top_n=top)
    if ctx.obj.get("format") == "json":
        report = ReportGenerator.format_abandoned_json(results)
        click.echo(report)
    else:
        report = ReportGenerator.format_abandoned(results)
        click.echo(report, color=True)

@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def risk(ctx, top):
    """Calcula o score de risco (commits × autores) por arquivo."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_risk_score(top_n=top)
    if ctx.obj.get("format") == "json":
        report = ReportGenerator.format_risk_score_json(results)
        click.echo(report)
    else:
        report = ReportGenerator.format_risk_score(results)
        click.echo(report, color=True)


@cli.command(name="bus-factor")
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def bus_factor(ctx, top):
    """Calcula o bus factor (gargalo de autores) por arquivo."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_bus_factor(top_n=top)
    if ctx.obj.get("format") == "json":
        report = ReportGenerator.format_bus_factor_json(results)
        click.echo(report)
    else:
        report = ReportGenerator.format_bus_factor(results)
        click.echo(report, color=True)
    
def main():
    """Ponto de entrada principal do CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()