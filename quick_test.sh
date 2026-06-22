#!/bin/bash
# Script de teste rápido para o RepoHealth

echo "============================================"
echo "    Iniciando a Suite de Testes - RepoHealth"
echo "============================================"

# Executa pytest com verbose e cobertura
python3 -m pytest repohealth -v --cov=repohealth --cov-report=term-missing

echo "============================================"
echo "    Testes concluídos!"
echo "============================================"
