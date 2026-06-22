"""Módulo para análise de repositórios Git."""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

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
        self._file_commits = None
        self._file_authors = None
        self._file_last_mod = None

    def get_all_commits(self) -> List:
        """
        Retorna todos os commits do repositório.

        Returns:
            Lista de commits
        """
        try:
            return list(self.repo.iter_commits("--all"))
        except Exception:
            return []

    def _analyze_repo(self) -> None:
        """Executa a análise do repositório em uma única passada e armazena em cache."""
        if self._file_commits is not None:
            return

        self._file_commits = {}
        self._file_authors = {}
        self._file_last_mod = {}

        try:
            commits = self.repo.iter_commits("--all")
        except Exception:
            return

        for commit in commits:
            try:
                commit_date = datetime.fromtimestamp(
                    commit.committed_date
                )
                author = commit.author.email

                for file_path in commit.stats.files:
                    # Contagem de commits
                    self._file_commits[file_path] = (
                        self._file_commits.get(file_path, 0) + 1
                    )

                    # Autores
                    if file_path not in self._file_authors:
                        self._file_authors[file_path] = set()
                    self._file_authors[file_path].add(author)

                    # Última modificação
                    if (
                        file_path not in self._file_last_mod
                        or commit_date > self._file_last_mod[file_path]
                    ):
                        self._file_last_mod[file_path] = commit_date
            except Exception:
                continue

    def get_file_commit_count(self) -> Dict[str, int]:
        """
        Conta quantos commits modificaram cada arquivo.

        Returns:
            Dicionário {arquivo: quantidade_commits}
        """
        self._analyze_repo()
        return self._file_commits

    def get_file_authors(self) -> Dict[str, Set[str]]:
        """
        Identifica quais autores modificaram cada arquivo.

        Returns:
            Dicionário {arquivo: set(autores)}
        """
        self._analyze_repo()
        return self._file_authors

    def get_file_last_modification(self) -> Dict[str, datetime]:
        """
        Identifica quando cada arquivo foi modificado pela última vez.

        Returns:
            Dicionário {arquivo: datetime}
        """
        self._analyze_repo()
        return self._file_last_mod

    def get_all_tracked_files(self) -> List[str]:
        """
        Retorna a lista de todos os arquivos rastreados pelo Git no branch atual.

        Returns:
            Lista de caminhos de arquivos
        """
        return [
            item.path
            for item in self.repo.tree().traverse()
            if item.type == "blob"
        ]
