# Migração do repositório atual para Django

Faça a mudança em uma branch separada, não diretamente na `main`.

```bash
git checkout main
git pull
git checkout -b feature/django-structure
```

## O que muda

1. `back-end/models`, `routes` e `services` deixam de ser arquivos/pastas genéricas e passam a ser apps Django reais.
2. `front-end/css`, `js` e `assets` passam para `static/`.
3. HTML passa para `templates/`.
4. Os bancos `usuarios`, `admin` e `livros` são consolidados em um banco único (`raiz_db`).
5. O esquema passa a ser versionado por `models.py` e `migrations/`, não por dumps SQL de produção.
6. A tabela `administradores` com senha própria não deve ser mantida como sistema de autenticação. Use `usuarios.User`/Django Auth.
7. Os SQL antigos ficam em `database/legacy/` somente para referência.

## Dados antigos

Os dumps fornecidos não continham registros, apenas estrutura. Se futuramente houver dados reais, crie uma **data migration** ou script de importação. Não envie dados pessoais reais para um repositório público.

## Após copiar os arquivos

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

Depois:

```bash
git add .
git commit -m "feat: cria estrutura inicial Django"
git push -u origin feature/django-structure
```

Abra um Pull Request para `main` e revise antes do merge.
