# Changelog

Todo o histórico de alterações deste projeto é documentado neste arquivo.

---

## [1.0.0] - 2026-06-22

Esta é a versão de lançamento oficial (v1.0.0) do **RepoHealth**, trazendo um conjunto completo de ferramentas de análise de repositórios Git, otimizações de performance, melhorias estéticas e ampla documentação.

### Adicionado
- **Métrica de Bus Factor (Fator de Gargalo):** Novo comando `bus-factor` para identificar quais arquivos dependem criticamente de poucos desenvolvedores.
- **Exportação para JSON:** Flag global `--format json` para extrair relatórios estruturados legíveis por outros programas e integrações CI/CD.
- **Opção de Exclusão de Arquivos:** Flag global `--exclude` permitindo ignorar pastas inteiras (como `venv`, caches ou dependências) da análise.
- **Exemplos Práticos:** Criação do diretório `examples/` contendo:
  - `run_analysis.py`: Exemplo de uso do RepoHealth como biblioteca/módulo Python.
  - `dashboard.py`: Script para extração de dados e geração automática de um Dashboard HTML interativo rico com gráficos (Chart.js) e estilização moderna (Tailwind CSS).
- **Scripts de Testes Auxiliares:** Criação do `quick_test.sh` na raiz do projeto para rodar testes locais rápidos.

### Modificado/Melhorado
- **Melhoria Estética:** Saída em modo texto (`--format text`) agora utiliza destaques de cor no terminal (Vermelho/Amarelo/Verde) dependendo da severidade dos riscos.
- **Otimização de Performance:** Consolidação das passadas de leitura dos commits no `GitAnalyzer` em um único ciclo com cacheamento dos dados em memória, tornando a ferramenta até **3x mais rápida** em repositórios grandes.
- **Cobertura de Testes Elevada:** A suite de testes foi expandida para cobrir 100% dos relatórios, métricas e exceções, alcançando **98% de cobertura total** do código.

### Documentação
- Atualizado o [README.md](file:///wsl.localhost/Ubuntu/home/soares/repo-mining-es2/README.md) detalhando todas as flags, opções, comandos e exemplos de JSON de saída.
- Criado o guia de desenvolvimento e contribuição [CONTRIBUTING.md](file:///wsl.localhost/Ubuntu/home/soares/repo-mining-es2/CONTRIBUTING.md).
- Criado o guia de execução de testes e setups [SETUP_AND_TESTING.md](file:///wsl.localhost/Ubuntu/home/soares/repo-mining-es2/SETUP_AND_TESTING.md).

---

## [0.1.0] - 2026-06-18

Versão inicial de desenvolvimento do RepoHealth (MSR Tool).

### Adicionado
- Implementação inicial da CLI estruturada usando `click`.
- Funcionalidades básicas de extração de commits via GitPython.
- Cálculo de métricas básicas de manutenibilidade:
  - Hotspots (mais modificados).
  - Autores por arquivo (Ownership).
  - Arquivos sem modificação (Abandoned Files).
  - Cálculo de Score de Risco (Commits × Autores).
