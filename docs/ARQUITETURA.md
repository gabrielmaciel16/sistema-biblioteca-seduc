# Arquitetura inicial

```text
Navegador
  HTML + CSS + JavaScript
           |
           | HTTP/HTTPS
           v
        Django
  URLs -> Views -> Forms/Services -> Models/ORM
           |
           v
          MySQL
```

## Regra principal

O frontend **não acessa o MySQL diretamente**. Toda leitura/escrita passa pelo Django, onde autenticação, autorização, validação e regras de negócio são aplicadas.

## Apps

- `usuarios`: autenticação, perfis e tipos de usuário.
- `escolas`: separação lógica entre instituições.
- `livros`: catálogo e estoque.
- `emprestimos`: regras de empréstimo/devolução.

## Segurança

- Senhas são armazenadas pelo sistema de hash do Django.
- Cadastro público cria somente `ALUNO`.
- Administradores devem ser criados pelo admin/superusuário.
- CSRF middleware está ativo e todos os formulários POST usam `{% csrf_token %}`.
- A aplicação usa o ORM; evite montar SQL com strings.
- Regras de autorização devem ficar no backend, nunca apenas em JavaScript.
- `SECRET_KEY` e senha do banco ficam em `.env`, que é ignorado pelo Git.
