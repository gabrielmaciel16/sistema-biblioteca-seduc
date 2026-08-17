# Raiz — Sistema de Biblioteca Escolar (Django)

Primeira estrutura Django para o projeto de gerenciamento de livros e empréstimos voltado inicialmente a escolas.

## Stack

- Python
- Django 5.2
- MySQL 8.0.11+ **ou** MariaDB 10.5+
- HTML + CSS + JavaScript
- Git/GitHub

## Arquitetura

```text
HTML/CSS/JS -> Django -> ORM -> MySQL
```

O navegador nunca acessa o banco diretamente.

## Estrutura

```text
config/          configurações Django
usuarios/        login, usuários e perfil de aluno
escolas/         instituições
livros/          catálogo
emprestimos/     empréstimos/devoluções e regras de negócio
templates/       HTML
static/          CSS, JS e imagens
database/        scripts locais e dumps antigos de referência
docs/            documentação
```

## 1. Pré-requisitos

- Python compatível com Django 5.2.
- MySQL 8.0.11+ ou MariaDB 10.5+.
- Git.

> Atenção: os dumps antigos enviados indicam MariaDB 10.4.32, que deve ser atualizado para usar Django 5.2.

## 2. Ambiente virtual (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Variáveis de ambiente

```powershell
Copy-Item .env.example .env
```

Edite `.env`. Nunca faça commit desse arquivo.

## 4. Banco

Use `database/create_database_dev.sql` para criar `raiz_db` e o usuário local do projeto. Troque a senha do exemplo.

## 5. Migrations

Como este scaffold começa com um usuário customizado, configure tudo **antes do primeiro `migrate`**. Depois rode:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## 6. Superusuário

```powershell
python manage.py createsuperuser
```

O login usa **e-mail + senha**.

## 7. Testes

```powershell
python manage.py test
```

## 8. Executar localmente

```powershell
python manage.py runserver
```

Abra `http://127.0.0.1:8000/entrar/`.

## Autenticação

- Senhas são tratadas pelo Django Auth; não são comparadas nem armazenadas manualmente.
- Cadastro público cria somente contas de aluno.
- Administradores/funcionários devem ser promovidos por um superusuário no `/admin/`.
- O modelo de usuário é definido em `usuarios.User` e usa o e-mail como identificador.

## Banco antigo

Os SQL enviados foram preservados em `database/legacy/` para consulta. Eles não devem ser tratados como o esquema oficial do Django daqui em diante. O esquema oficial será `models.py` + migrations.

## Antes de produção

- `DEBUG=False`
- `SECRET_KEY` forte e privada
- HTTPS
- banco não exposto diretamente à internet
- backups
- permissões por escola
- executar `python manage.py check --deploy`
- usar servidor WSGI/ASGI de produção em vez de `runserver`

Leia `docs/ARQUITETURA.md` e `docs/MIGRACAO_DO_REPOSITORIO_ATUAL.md` antes de integrar este scaffold à `main`.
