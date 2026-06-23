# RepoHealth – Análise de Saúde de Repositórios Git

[![Tests](https://github.com/belisco/repo-mining-es2/actions/workflows/tests.yml/badge.svg)](https://github.com/belisco/repo-mining-es2/actions/workflows/tests.yml)

## Integrantes

- Gustavo Amaral Bernardino
- João Vitor Soares Santos
- Luis Felipe Belasco Silva
- Lean Henrique Pereira Miranda

---

## Objetivo

**RepoHealth** é uma ferramenta de linha de comando para minerar e analisar a saúde de repositórios Git. Ela extrai o histórico de commits, dados de autoria e datas de modificação para identificar riscos de manutenção, hotspots e gargalos de desenvolvimento.

A ferramenta apoia a identificação dos seguintes sinais críticos:

- **Hotspots** – arquivos modificados com alta frequência.
- **Autoria (Ownership)** – quantidade de autores diferentes que modificaram cada arquivo.
- **Abandono (Abandoned Files)** – arquivos sem modificações há mais tempo.
- **Score de Risco (Risk Score)** – correlação entre quantidade de commits e número de autores (Commits × Autores).
- **Fator de Gargalo (Bus Factor)** – o número mínimo de desenvolvedores responsáveis por mais de 50% das alterações de um arquivo.

---

## Funcionalidades e Diferenciais

- **Análise Otimizada:** Varredura em uma única passada pelos commits do Git com cache integrado, reduzindo o tempo de análise em repositórios grandes.
- **Destaques Coloridos:** Visualização intuitiva no terminal (arquivos de alto risco destacados em vermelho, alertas médios em amarelo e arquivos saudáveis em verde).
- **Filtros de Exclusão:** Suporte a ignorar arquivos e pastas específicos da análise (como ambientes virtuais, dependências ou arquivos de configuração).
- **Exportação JSON:** Geração de relatórios estruturados para fácil integração com pipelines de CI/CD ou outras ferramentas externas.

---

## Como Instalar

**Pré-requisitos:** Python 3.12+

1. Clone o repositório:
   ```bash
   git clone https://github.com/belisco/repo-mining-es2.git
   cd repo-mining-es2
   ```

2. Instale o pacote localmente em modo editável:
   ```bash
   cd repohealth
   pip install -e .
   ```
   *Ou instale diretamente as dependências:*
   ```bash
   pip install -r repohealth/requirements.txt
   ```

---

## Como Utilizar

A ferramenta pode ser executada utilizando o comando instalado `repohealth` ou diretamente via módulo Python:
```bash
python3 -m repohealth.cli [OPÇÕES_GLOBAIS] COMANDO [OPÇÕES_DO_COMANDO]
```

### Opções Globais
- `--repo PATH` – Define o caminho do repositório Git a analisar (padrão: `.` - diretório atual).
- `--format [text|json]` – Formato do relatório impresso (padrão: `text`).
- `--exclude PATTERNS` – Filtra arquivos/diretórios da análise usando padrões separados por vírgula (ex: `venv/*,*.json`).

---

### Comandos Disponíveis

#### 1. hotspots
Identifica os arquivos que sofreram mais modificações ao longo da história do repositório.
* **Opções:** `--top N` (padrão: 10).
* **Exemplo de uso:**
  ```bash
  python3 -m repohealth.cli hotspots --top 5
  ```

#### 2. ownership
Calcula o número de autores distintos que alteraram cada arquivo do projeto.
* **Opções:** `--top N` (padrão: 10).
* **Exemplo de uso:**
  ```bash
  python3 -m repohealth.cli ownership --top 5
  ```

#### 3. abandoned
Aponta quais arquivos estão há mais tempo sem receber novas modificações.
* **Opções:** `--top N` (padrão: 10).
* **Exemplo de uso:**
  ```bash
  python3 -m repohealth.cli abandoned
  ```

#### 4. risk
Calcula o Score de Risco dos arquivos baseado na fórmula `commits * autores`. Arquivos muito modificados por muitos autores tendem a possuir alta complexidade e risco.
* **Opções:** `--top N` (padrão: 10).
* **Exemplo de uso:**
  ```bash
  python3 -m repohealth.cli risk --top 3
  ```

#### 5. bus-factor
Determina a vulnerabilidade de dependência de autores em cada arquivo. O Bus Factor indica a quantidade mínima de desenvolvedores cuja saída inviabilizaria a manutenção daquele arquivo (calculado pela menor quantidade de autores que cobrem mais de 50% dos commits).
* **Opções:** `--top N` (padrão: 10).
* **Exemplo de uso:**
  ```bash
  python3 -m repohealth.cli bus-factor
  ```

---

### Seção de Exportação (Exemplo JSON)

Para exportar as métricas obtidas e alimentar painéis externos ou ferramentas de BI, utilize a flag `--format json`:
```bash
python3 -m repohealth.cli --format json bus-factor --top 2
```

**Exemplo de Retorno:**
```json
[
  {
    "file": "repohealth/git_analyzer.py",
    "bus_factor": 1,
    "main_author": "soares@example.com",
    "main_author_percentage": 90.0,
    "total_commits": 10
  },
  {
    "file": "README.md",
    "bus_factor": 2,
    "main_author": "belisco@example.com",
    "main_author_percentage": 50.0,
    "total_commits": 8
  }
]
```

---

## Como Executar os Testes

Para validar a integridade do código e rodar a suite de testes automatizados com cobertura:
```bash
python3 -m pytest repohealth
```

---

## Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
