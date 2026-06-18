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
    
    def get_all_commits(self) -> List:
        """
        Retorna todos os commits do repositório.

        Returns:
            Lista de commits
        """
        return list(self.repo.iter_commits("--all"))
    
    def get_file_commit_count(self) -> Dict[str, int]:
        """
        Conta quantos commits modificaram cada arquivo.

        Returns:
            Dicionário {arquivo: quantidade_commits}
        """
        file_commits = {}

        for commit in self.repo.iter_commits("--all"):
            try:
                if commit.parents:
                    diffs = commit.parents[0].diff(commit)
                    for diff in diffs:
                        file_path = diff.b_path if diff.b_path else diff.a_path
                        if file_path:
                            file_commits[file_path] = file_commits.get(file_path, 0) + 1
            except Exception:
                continue

        return file_commits