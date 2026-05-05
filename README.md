# TP: Mineração de Repositórios de Software

## 1. Membros do Grupo

* Gustavo Amaral Bernardino
* João Vitor Soares Santos
* Luis Felipe Belasco Silva
* Lean Henrique Pereira Miranda


## 2. Explicação do Sistema

O sistema consiste em uma ferramenta de linha de comando voltada para a mineração de repositórios de software, com o objetivo de identificar possíveis problemas de manutenção.

A aplicação analisa dados provenientes de repositórios Git ou GitHub, considerando diferentes artefatos como commits, código-fonte, issues, pull requests e histórico de alterações. A partir dessas informações, o sistema extrai métricas e padrões que podem indicar problemas como alta complexidade, baixa qualidade de código ou riscos de manutenção.

Os resultados são apresentados de forma estruturada, podendo incluir métricas quantitativas e visualizações que auxiliam na análise do estado do software.


## 3. Tecnologias Utilizadas

Inicialmente, pensamos em avaliar repositorios em python, então separamos algumas opções que parecem encaixar com o que pensamos nesse primeiro momento:

* **Mineração de repositórios**: PyDriller e GitPython
* **Integração com GitHub**: PyGithub, GitHub REST API
* **Interface de linha de comando (CLI)**: Typer ou argparse
* **Análise de código (parsers)**: Python AST
* **Análise de histórico**: PyDriller, CodeShovel e GitEvo
* **Métricas de software**: Lizard, Radon, CLOC
* **Qualidade de código**: Flake8
* **Segurança**: Bandit
