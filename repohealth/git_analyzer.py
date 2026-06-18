"""Módulo para análise de repositórios."""

from pathlib import Path
from git import Repo


class GitAnalyzer:
    """Classe responsável por analisar repositórios Git."""

    def __init__(self, repo_path: str = "."):
        """
        Inicializa o analisador com o caminho do repositório.

        Args:
            repo_path: Caminho para o repositório Git
        """
        self.repo_path = Path(repo_path)
        self.repo = Repo(repo_path)