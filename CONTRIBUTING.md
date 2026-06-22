# Como Contribuir para o RepoHealth

Obrigado pelo seu interesse em contribuir para o **RepoHealth**! A sua ajuda é muito importante para manter o projeto saudável e útil.

Aqui estão as diretrizes básicas para guiar a sua contribuição.

---

## 1. Processo de Contribuição

1. **Fork o repositório:** Crie uma cópia do projeto na sua conta do GitHub.
2. **Crie uma branch para a sua alteração:**
   ```bash
   git checkout -b feat/nome-da-funcionalidade
   ```
   *Para correções de bugs, use o prefixo `fix/`.*
3. **Desenvolva as modificações:** Certifique-se de escrever testes unitários cobrindo o novo código.
4. **Execute a suite de testes localmente:** Garanta que todas as validações passem (detalhes na seção abaixo).
5. **Faça o Commit:** Envie suas modificações locais seguindo as regras de commits (detalhes abaixo).
6. **Submeta um Pull Request (PR):** Abra uma proposta de merge apontando para a branch `main` do repositório original.

---

## 2. Padrões de Código e Estilo

Para manter a base de código limpa e legível, seguimos as seguintes convenções:

* **Estilo PEP 8:** Escreva código Python limpo e bem formatado.
* **Tipagem Estática (Type Hints):** Sempre que possível, declare os tipos de argumentos e retornos das funções.
* **Docstrings:** Use docstrings em todas as classes e métodos públicos detalhando a funcionalidade, argumentos e retornos.
* **Mensagens de Commit:** Adotamos o padrão de **Conventional Commits**. Exemplos:
  - `feat: ...` (para novas funcionalidades)
  - `fix: ...` (para correção de bugs)
  - `docs: ...` (para documentação)
  - `refactor: ...` (para refatorações de código)
  - `style: ...` (para estilizações no terminal ou formatações estéticas)
  - `chore: ...` (para tarefas auxiliares, build, etc.)

---

## 3. Como Rodar os Testes

Toda contribuição deve incluir testes e manter ou elevar a cobertura de testes do projeto.

Execute o script de validação rápida na raiz do projeto:
```bash
./quick_test.sh
```

Ou execute o comando de cobertura manualmente:
```bash
python3 -m pytest repohealth --cov=repohealth --cov-report=term-missing
```

A aprovação no GitHub Actions (CI/CD) é obrigatória para que o Pull Request seja aprovado.

---

## 4. Processo de Release

Para cortar uma nova versão do RepoHealth:

1. **Atualize a versão:** Altere `__version__` em `repohealth/__init__.py`. `setup.py` e `pyproject.toml` leem esse valor automaticamente, então não precisam ser editados.
2. **Atualize o CHANGELOG.md:** Adicione uma seção descrevendo as mudanças da nova versão.
3. **Commit:** `chore: prepare vX.Y.Z release`.
4. **Crie a tag:** `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.
5. **Publique:** `git push && git push --tags`.
