# Banco de dados

O Django passa a ser a **fonte principal do esquema** através de `models.py` + migrations.

## Banco recomendado

Use um único banco, por exemplo `raiz_db`. Isso simplifica relacionamentos, migrations, testes e deploy.

Os dumps antigos (`usuarios`, `admin` e `livros`) ficam em `database/legacy/` apenas como referência histórica. Não versionem dumps com dados reais de alunos/usuários.

## Compatibilidade importante

Os dumps enviados foram gerados por um servidor identificado como **MariaDB 10.4.32**. Django 5.2 requer MariaDB 10.5+ ou MySQL 8.0.11+. Portanto, atualize o servidor antes de usar este scaffold com Django 5.2.

## Criação local

1. Edite a senha em `create_database_dev.sql`.
2. Execute o script no MySQL/MariaDB compatível.
3. Copie `.env.example` para `.env` e use a mesma senha.
4. Rode `python manage.py makemigrations` e `python manage.py migrate`.
