"""CLI para a ferramenta RepoHealth."""

import sys
from pathlib import Path

import click


@click.group()
def cli():
    """RepoHealth - Ferramenta de análise de saúde de repositórios Git."""
    pass


def main():
    """Ponto de entrada principal do CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()