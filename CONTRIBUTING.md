# Como contribuir

## Branches

Não programe diretamente na `main`.

- `feature/nome-da-funcionalidade`
- `fix/nome-do-bug`
- `docs/nome-da-documentacao`

## Fluxo

1. Atualize a `main`.
2. Crie sua branch.
3. Faça alterações pequenas e testáveis.
4. Rode `python manage.py test`.
5. Faça commits claros.
6. Envie a branch e abra Pull Request.
7. Outra pessoa revisa antes do merge.

## Commits

- `feat: ...` nova funcionalidade
- `fix: ...` correção
- `docs: ...` documentação
- `test: ...` testes
- `refactor: ...` reorganização sem mudar comportamento

## Segurança

Nunca faça commit de `.env`, senhas, chaves, tokens, CPF, dados reais de alunos ou backups de produção.
