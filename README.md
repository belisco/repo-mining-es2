# 📊 MSR Tool – Análise de Manutenibilidade

## 👥 Integrantes

- Gustavo Amaral Bernardino  
- João Vitor Soares Santos  
- Luis Felipe Belasco Silva  
- Lean Henrique Pereira Miranda  

---

## 🎯 Objetivo

Desenvolver uma ferramenta de linha de comando para identificar problemas reais de manutenção em repositórios Python, combinando análise de código com histórico de commits.

O foco não é apenas coletar métricas, mas apontar onde estão os riscos de evolução do software.

---

## ❗ Recorte do Problema

Em vez de analisar tudo de forma superficial, o projeto foca em um problema específico:

> Quais arquivos do sistema são mais difíceis de manter e por quê?

Para responder isso, vamos investigar três sinais principais:

- Complexidade do código  
- Frequência de mudanças  
- Volume de alterações (code churn)  

Hipótese:

> Arquivos complexos que mudam com frequência tendem a ser os principais gargalos de manutenção.

---

## 🧠 Abordagem Proposta

A ferramenta será dividida em três etapas:

### 1. Extração de histórico

Uso do PyDriller para coletar:

- Commits  
- Arquivos modificados  
- Linhas adicionadas/removidas  

---

### 2. Análise de código

Aplicação de métricas estruturais:

- Complexidade ciclomática (Radon)  
- Linhas de código (CLOC)  

---

### 3. Correlação

Os dados serão combinados para identificar:

- Hotspots (arquivos muito alterados)  
- Arquivos complexos  
- Arquivos críticos (interseção dos dois)  

---

## ⚙️ Decisões de Projeto

### Linguagem: Python
Permite integração direta com ferramentas de análise e parsing (AST), além de simplificar o desenvolvimento.

---

### Fonte de dados: Git (local)
Optamos inicialmente por repositórios locais para:

- evitar dependência de API  
- reduzir complexidade  
- focar na análise  

---

### Interface: CLI
Uso de Typer para criar uma ferramenta simples e automatizável.

---

### Escopo inicial reduzido

Não vamos analisar tudo (issues, PRs, CI etc.) neste momento.

Foco em:

- código  
- commits  

---

## 📊 Saída Esperada

### Terminal

```text
payment.py → Complexidade alta + muitas mudanças → RISCO ALTO
