# MSR Tool – Análise de Manutenibilidade de Repositórios

## Integrantes

- Gustavo Amaral Bernardino
- João Vitor Soares Santos
- Luis Felipe Belasco Silva
- Lean Henrique Pereira Miranda

---

## Objetivo

MSR Tool é uma ferramenta de linha de comando para identificar problemas reais de manutenção em repositórios Python. Ela combina análise estática de código com histórico de commits para responder: **quais arquivos são mais difíceis de manter e por quê?**

A ferramenta cruza três sinais para detectar riscos de evolução:

- **Complexidade do código** – via complexidade ciclomática e índice de manutenibilidade
- **Frequência de mudanças** – quantas vezes cada arquivo foi modificado
- **Volume de alterações (code churn)** – linhas adicionadas e removidas por arquivo

Arquivos complexos que mudam com frequência são apontados como **hotspots críticos**.

---

## Tecnologias Utilizadas

| Tecnologia | Papel |
|---|---|
| Python 3.12+ | Linguagem principal |
| [PyDriller](https://github.com/ishepard/pydriller) | Extração de histórico de commits via Git |
| [Radon](https://radon.readthedocs.io/) | Cálculo de complexidade ciclomática e índice de manutenibilidade |
| [Typer](https://typer.tiangolo.com/) | Interface de linha de comando |
| [Poetry](https://python-poetry.org/) | Gerenciamento de dependências |
| [pytest](https://docs.pytest.org/) | Execução de testes |
| GitHub Actions | Integração contínua e execução automática de testes |

---

## Como Instalar

**Pré-requisitos:** Python 3.12+ e [Poetry](https://python-poetry.org/docs/#installation)

```bash
git clone https://github.com/<seu-usuario>/msr-tool.git
cd msr-tool
poetry install
```

---

## Como Utilizar

### Analisar um repositório local

```bash
poetry run msr analyze --repo /caminho/para/o/repositorio
```

### Analisar um repositório remoto

```bash
poetry run msr analyze --repo https://github.com/usuario/projeto.git
```

### Opções disponíveis

```bash
poetry run msr analyze --help
```

```
Usage: msr analyze [OPTIONS]

Options:
  --repo TEXT      Caminho local ou URL do repositório Git  [required]
  --top INTEGER    Número de arquivos a exibir (padrão: 10)
  --since TEXT     Data de início da análise (formato: YYYY-MM-DD)
  --help           Exibe esta mensagem e sai
```

### Exemplo de saída

```
Arquivo                  Complexidade  Mudanças  Churn    Risco
────────────────────────────────────────────────────────────────
src/payment.py           Alta (18)     47        +3.2k    CRÍTICO
src/auth/session.py      Média (9)     31        +1.8k    ALTO
src/utils/formatter.py   Baixa (3)     28        +900     MÉDIO
```

---

## Como Executar os Testes

```bash
poetry run pytest
```

Para ver a cobertura de testes:

```bash
poetry run pytest --cov=msr_tool
```

Os testes também são executados automaticamente via GitHub Actions a cada push ou pull request.
