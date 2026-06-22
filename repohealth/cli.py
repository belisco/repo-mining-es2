"""CLI para a ferramenta RepoHealth."""


from .git_analyzer import GitAnalyzer
from .metrics import MetricsCalculator
from .reports import ReportGenerator
import sys
from pathlib import Path

import click


@click.group()
@click.option("--repo", default=".", help="Caminho para o repositório Git")
@click.pass_context
def cli(ctx, repo):
    """RepoHealth - Ferramenta de análise de saúde de repositórios Git."""
    ctx.ensure_object(dict)
    
    # Valida se é um repositório Git
    repo_path = Path(repo)
    if not (repo_path / ".git").exists():
        click.echo(f"Erro: '{repo}' não é um repositório Git válido.", err=True)
        sys.exit(1)
    
    # Inicializa analisadores
    ctx.obj["analyzer"] = GitAnalyzer(repo)
    ctx.obj["calculator"] = MetricsCalculator(ctx.obj["analyzer"])


@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def hotspots(ctx, top):
    """Identifica os arquivos mais modificados (hotspots)."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_hotspots(top_n=top)
    report = ReportGenerator.format_hotspots(results)
    click.echo(report)

@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def ownership(ctx, top):
    """Identifica a quantidade de autores por arquivo."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_ownership(top_n=top)
    report = ReportGenerator.format_ownership(results)
    click.echo(report)
    
@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def abandoned(ctx, top):
    """Mostra arquivos sem modificações há mais tempo."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_abandoned(top_n=top)
    report = ReportGenerator.format_abandoned(results)
    click.echo(report)

@cli.command()
@click.option("--top", default=10, help="Número de resultados a exibir")
@click.pass_context
def risk(ctx, top):
    """Calcula o score de risco (commits × autores) por arquivo."""
    calculator = ctx.obj["calculator"]
    results = calculator.calculate_risk_score(top_n=top)
    report = ReportGenerator.format_risk_score(results)
    click.echo(report)
    
def main():
    """Ponto de entrada principal do CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()