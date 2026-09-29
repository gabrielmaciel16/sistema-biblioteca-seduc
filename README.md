# Sistema da biblioteca Multimeios

Projeto de aprendizagem para o Multimeios da **EEEP Presidente Roosevelt**. Permite cadastrar alunos e livros, registrar empréstimos e devoluções e consultar o histórico. Um registro de livro representa um título/edição e informa a quantidade de exemplares. Não inclui importação automática do acervo antigo.

## O que há no projeto

Usamos Python, Django, HTML, CSS e **um banco SQLite** local. O Django cria e mantém as tabelas por meio das migrations. O administrador usa o sistema de usuários que já vem com o Django. O cadastro de alunos é independente do login: estudantes não precisam de senha para constar no catálogo de empréstimos.

```text
manage.py                 comandos do Django
requirements.txt          dependências Python
config/settings.py        configuração local e banco SQLite
config/urls.py            entrada das URLs e login
biblioteca/models.py      tabelas Aluno, Livro e Emprestimo
biblioteca/forms.py       formulários e validações
biblioteca/views.py       páginas e regras de empréstimo/devolução
biblioteca/urls.py        caminhos das páginas
biblioteca/admin.py       reserva padrão do Django; contas em /admin/
biblioteca/migrations/    versão inicial das tabelas
templates/                páginas HTML
static/css/style.css      aparência das páginas
```

## Instalação passo a passo

1. Instale **Python 3.10 ou superior** em [python.org](https://www.python.org/downloads/) e Git. No Windows, marque a opção de adicionar Python ao PATH. Confirme com `py --version` (Windows) ou `python3 --version` (macOS/Linux).
2. Clone o projeto e entre na pasta:

```bash
git clone https://github.com/gabrielmaciel16/sistema-biblioteca-seduc.git
cd sistema-biblioteca-seduc
```

Se estiver estudando esta versão antes de ela ser integrada à `main`, execute `git switch refatoracao-versao-iniciante`.

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abra **http://127.0.0.1:8000/** no navegador. Entre com o usuário e a senha criados no comando `createsuperuser`. Os dados ficam no arquivo local `db.sqlite3`, que não é enviado ao GitHub. Para parar o servidor, pressione `Ctrl+C`. Para voltar a trabalhar depois, ative `.venv` e rode `python manage.py runserver`.

Se você mudar um modelo, rode `python manage.py makemigrations` e `python manage.py migrate`, depois envie o arquivo de migration criado junto com o código. Verifique com `python manage.py check` e `python manage.py test`.

## Como usar

1. Cadastre alunos e livros. Ao cadastrar um livro, a quantidade disponível começa igual à quantidade total.
2. Clique em **Registrar empréstimo**, escolha aluno e livro e informe a data prevista.
3. Na lista de empréstimos ativos, clique em **Devolver**. A data de devolução é registrada e um exemplar volta ao estoque.
4. Consulte o histórico. Empréstimos ativos com prazo vencido aparecem como **Atrasado** na tela; continuam ativos até a devolução.

Um aluno ou livro com empréstimos registrados não pode ser excluído, pois isso apagaria a referência do histórico. A edição do total de livros preserva quantos exemplares estão emprestados. Não cadastre empréstimos diretamente no banco: utilize as páginas do sistema para manter o estoque correto.

## Como estudar este projeto

1. Leia `biblioteca/models.py`: cada classe representa uma tabela e as chaves ligam o empréstimo a aluno e livro.
2. Leia `biblioteca/forms.py`: os formulários escolhem os campos e validam entradas.
3. Leia `biblioteca/views.py`: cada função recebe uma requisição, consulta ou altera dados e entrega uma página ou redirecionamento. Veja `emprestimo_novo` e `devolver` para entender o estoque.
4. Leia `biblioteca/urls.py` e `config/urls.py`: ligam endereços às funções.
5. Abra `templates/`: `base.html` fornece o menu; cada página estende essa base.
6. Leia `static/css/style.css`: contém somente a apresentação visual.

Experimente criar um aluno e um livro de teste. Abra cada URL e encontre a função e o template correspondentes. Depois execute os testes em `biblioteca/tests.py`.

### Recursos do Django que aparecem no código

- `@staff_member_required`: permite que somente usuários marcados como **Membro da equipe** acessem as páginas. É um recurso pronto do Django.
- `transaction.atomic()`: mantém as duas alterações de um empréstimo ou devolução juntas. Se uma falhar, nenhuma fica salva pela metade.
- `F("quantidade_disponivel")`: faz a conta do estoque diretamente no banco. Com a condição `quantidade_disponivel__gt=0`, dois pedidos não retiram o mesmo último exemplar.
- `on_delete=models.PROTECT`: impede a exclusão de aluno ou livro que aparece no histórico.
- `migrations/`, `__init__.py`, `asgi.py` e `wsgi.py`: são arquivos normais de um projeto Django. Para começar, basta estudar os arquivos da ordem acima; não é necessário editá-los.

O Django Admin em `/admin/` serve para criar contas da equipe. O catálogo e os empréstimos são gerenciados nas páginas do sistema, evitando dois lugares com regras diferentes de estoque.

## Banco antigo e futura migração

Esta branch cria **um esquema novo** com SQLite e o usuário padrão do Django. As migrations antigas (`usuarios`, `livros`, `emprestimos`, `escolas`) e os scripts SQL dos três bancos anteriores não são compatíveis com a nova migration inicial. **Não execute esta versão sobre um banco antigo com dados esperando que os dados sejam convertidos automaticamente.** Os arquivos antigos permanecem no histórico da branch `main` e do Git; a documentação anterior indicava que os dumps fornecidos continham somente estrutura, mas confirme isso em qualquer instalação real antes de migrar. Faça backup, mapeie identificadores e relações, importe os dados em uma cópia e confira quantidades e empréstimos antes de trocar a instalação em uso.

Para migrar **futuramente** para MySQL, primeiro instale um servidor compatível e um driver Python (`mysqlclient`), crie um banco vazio com `utf8mb4` e altere `DATABASES` em `config/settings.py` para `django.db.backends.mysql` com nome, usuário, senha, host e porta. Rode `python manage.py migrate` nesse banco novo. Isso cria as tabelas, mas **não transfere** automaticamente os dados do SQLite; planeje e teste a exportação/importação separadamente. Nunca coloque senhas no repositório.

## Limites desta versão

Ela foi feita para estudo e uso local inicial. Para colocar na internet, altere `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` em `config/settings.py`, configure HTTPS, backups e um servidor de aplicação adequado. Não use `runserver` como servidor público. Crie usuários de equipe pelo admin e marque **Membro da equipe** (`is_staff`); não existe cadastro público de administradores.
