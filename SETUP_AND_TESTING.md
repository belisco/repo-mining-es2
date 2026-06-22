# Guia de Configuração e Testes

Este guia descreve como configurar o ambiente de desenvolvimento do **RepoHealth** e como executar sua suite de testes com relatórios de cobertura de código.

---

## 1. Configuração do Ambiente

O projeto requer **Python 3.12+**. 

### Passo 1: Instalar Dependências
Instale as dependências listadas no arquivo `repohealth/requirements.txt`:

```bash
pip install -r repohealth/requirements.txt
```

### Passo 2: Instalar em Modo Editável (Opcional)
Para poder rodar o comando global `repohealth` direto do terminal em qualquer diretório:

```bash
pip install -e .
```

---

## 2. Estrutura da Suite de Testes

Os testes estão organizados dentro da pasta `repohealth/tests/` e utilizam o framework [pytest](https://docs.pytest.org/):

- **[test_git_analyzer.py](file:///wsl.localhost/Ubuntu/home/soares/repo-mining-es2/repohealth/tests/test_git_analyzer.py):** Valida a inicialização do GitAnalyzer, cacheamento de passadas e recuperação de dados de commits, autores e caminhos ignorados.
- **[test_metrics.py](file:///wsl.localhost/Ubuntu/home/soares/repo-mining-es2/repohealth/tests/test_metrics.py):** Valida o cálculo de hotspots, ownership, abandoned files, risk score e bus-factor (incluindo tratamento de limites `top_n`).
- **[test_reports.py](file:///wsl.localhost/Ubuntu/home/soares/repo-mining-es2/repohealth/tests/test_reports.py):** Testa a formatação das saídas (incluindo cores do terminal e saídas JSON estruturadas).
- **[test_cli.py](file:///wsl.localhost/Ubuntu/home/soares/repo-mining-es2/repohealth/tests/test_cli.py):** Simula chamadas de CLI completas e valida as flags globais (`--repo`, `--format`, `--exclude`, etc.).

---

## 3. Como Executar os Testes

Você pode executar os testes das seguintes maneiras:

### Execução Completa (Simples)
```bash
python3 -m pytest repohealth
```

### Execução Detalhada
```bash
python3 -m pytest repohealth -v
```

### Execução com Cobertura de Código (Coverage)
Para visualizar quais partes do código foram cobertas pelos testes diretamente no terminal:
```bash
python3 -m pytest repohealth --cov=repohealth --cov-report=term-missing
```

A suite está configurada para gerar relatórios detalhados em HTML na pasta `htmlcov/` se necessário.

---

## 4. Script de Teste Rápido

Para facilitar a validação local antes de realizar commits, foi fornecido o script auxiliar `quick_test.sh`.

Para executá-lo:
```bash
./quick_test.sh
```
