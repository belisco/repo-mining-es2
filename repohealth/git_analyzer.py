"""Módulo para análise de repositórios Git."""

from datetime import datetime
import fnmatch
from pathlib import Path
from typing import Dict, List, Set

from git import Repo


class GitAnalyzer:
    """Classe responsável por analisar repositórios Git."""

    def __init__(self, repo_path: str = ".", exclude_patterns: List[str] = None):
        """
        Inicializa o analisador com o caminho do repositório.

        Args:
            repo_path: Caminho para o repositório Git
            exclude_patterns: Padrões de exclusão de arquivos (glob/path)
        """
        self.repo_path = Path(repo_path)
        self.repo = Repo(repo_path)
        self.exclude_patterns = exclude_patterns or []
        self._file_commits = None
        self._file_authors = None
        self._file_last_mod = None

    def _is_excluded(self, file_path: str) -> bool:
        """Verifica se um arquivo corresponde a algum padrão de exclusão."""
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
            if pattern.endswith("/") and file_path.startswith(pattern):
                return True
            if file_path.startswith(pattern):
                return True
        return False

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
                    if self._is_excluded(file_path):
                        continue

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
            if item.type == "blob" and not self._is_excluded(item.path)
        ]
