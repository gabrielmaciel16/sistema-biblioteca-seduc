# Sistema da biblioteca Multimeios

Projeto de aprendizagem para o Multimeios da **EEEP Presidente Roosevelt**. Permite cadastrar alunos e livros, registrar empréstimos e devoluções e consultar o histórico. Um registro de livro representa um título/edição e informa a quantidade de exemplares. Não inclui importação automática do acervo antigo.

## O que há no projeto

Usamos Python, Django, HTML, CSS e **um banco MySQL ou SQLite**, escolhido pela configuração. O Django cria e mantém as tabelas por meio das migrations. O administrador usa o sistema de usuários que já vem com o Django. O cadastro de alunos é independente do login: estudantes não precisam de senha para constar no catálogo de empréstimos.

```text
manage.py                 comandos do Django
requirements.txt          dependências Python
requirements-mysql.txt    dependências Python, incluindo o driver MySQL
.env.example              modelo de configuração, sem senhas reais
.env                      configuração privada local (ignorada pelo Git)
config/settings.py        leitura do .env e escolha do banco
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

### 1. Preparar o ambiente Python

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Se você já tem um ambiente chamado `ll_env`, pode ativá-lo com `.\ll_env\Scripts\Activate.ps1` em vez de criar outro. Execute os comandos na pasta que contém `manage.py`.

### 2. Configurar o MySQL e o .env

O servidor MySQL precisa estar instalado e funcionando. O Workbench é uma interface de administração; instalar apenas o Workbench ou o pacote `mysqlclient` não instala o servidor. Use uma versão compatível com o [Django 5.2](https://docs.djangoproject.com/en/5.2/ref/databases/#mysql-notes).

Instale o driver no ambiente virtual ativo:

```powershell
python -m pip install -r requirements-mysql.txt
```

Esse arquivo também instala Django e `python-dotenv`. Se a instalação do `mysqlclient` exigir compilação, veja os [pré-requisitos oficiais para seu sistema](https://github.com/PyMySQL/mysqlclient#install). Não troque o driver sem verificar a compatibilidade.

Entre no MySQL com uma conta administrativa, pelo Workbench, phpMyAdmin ou cliente de terminal. **Execute o SQL abaixo no MySQL, não diretamente no PowerShell.** Ele cria um banco novo e uma conta local da aplicação; substitua a senha de exemplo antes de executar:

```sql
CREATE DATABASE biblioteca CHARACTER SET utf8mb4;
CREATE USER 'biblioteca_app'@'localhost' IDENTIFIED BY 'SUBSTITUA_POR_UMA_SENHA_FORTE';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, INDEX, REFERENCES
ON biblioteca.* TO 'biblioteca_app'@'localhost';
```

As permissões são limitadas ao banco `biblioteca` e permitem executar as migrations. Não conceda acesso global `*.*` nem use a conta administrativa no Django. Se esse banco ou usuário já existir, confira-o antes de continuar; não exclua bancos para contornar o erro. Use um banco vazio para esta estrutura nova. Criar ou alterar contas depende das permissões do administrador do MySQL.

No PowerShell, copie o modelo **somente se ainda não houver um `.env`**, para não sobrescrever sua configuração:

```powershell
Copy-Item .env.example .env
```

No macOS/Linux, o comando equivalente é `cp .env.example .env`. No VS Code, o `.env` deve ficar ao lado do `manage.py`, fora de `config` e do ambiente virtual. Edite:

```dotenv
DB_ENGINE=mysql
DB_NAME=biblioteca
DB_USER=biblioteca_app
DB_PASSWORD="SENHA_QUE_VOCE_CONFIGUROU_NO_MYSQL"
DB_HOST=localhost
DB_PORT=3306
```

`DB_NAME` é o banco; `DB_USER` é a conta do MySQL, não o usuário do Windows ou o login do site. A senha precisa ser a mesma criada para essa conta. `localhost` indica o próprio computador; `3306` é a porta padrão, se não foi alterada. **Preencher o `.env` não cria nem muda a senha no MySQL.**

O `config/settings.py` importa `load_dotenv`, lê `BASE_DIR / ".env"` antes de configurar `DATABASES` e acessa os valores com `os.environ`. Variáveis já definidas no ambiente do processo têm prioridade sobre o arquivo. O modo MySQL usa `utf8mb4` e validações estritas para reduzir o risco de truncar dados silenciosamente. Configuração incompleta gera um erro com os nomes dos campos pendentes, sem imprimir seus valores.

### Alternativa: continuar com SQLite

Para manter seu banco local, use `DB_ENGINE=sqlite` no `.env`. Nesse modo, os campos `DB_NAME`, `DB_USER` e `DB_PASSWORD` não são usados e não é necessário instalar `requirements-mysql.txt`. Sem `.env` e sem `DB_ENGINE` no ambiente, o projeto preserva o SQLite como padrão. Os dados ficam no arquivo `db.sqlite3`, ignorado pelo Git. Selecionar MySQL não copia os registros desse arquivo.

### 3. Criar as tabelas e iniciar o sistema

Salve os arquivos e execute no terminal, com o ambiente virtual ativo:

```powershell
python manage.py check --database default
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`migrate` cria ou atualiza as tabelas no banco selecionado; não cria o banco MySQL ou suas contas. `createsuperuser` cria o login administrativo **do site**, separado da conta MySQL. Abra **http://127.0.0.1:8000/** e entre com esse login. Para parar o servidor, pressione `Ctrl+C`. Para voltar a trabalhar depois, ative o ambiente e rode `python manage.py runserver`.

Se você mudar um modelo, rode `python manage.py makemigrations` e `python manage.py migrate`, depois envie o arquivo de migration criado junto com o código. Verifique com `python manage.py check` e `python manage.py test`.

Para rodar os testes com SQLite sem mudar seu `.env`, use no PowerShell:

```powershell
$env:DB_ENGINE = "sqlite"
python manage.py test
Remove-Item Env:DB_ENGINE
```

No macOS/Linux: `DB_ENGINE=sqlite python manage.py test`. O Django cria um banco separado para os testes. Testar com MySQL exige permissão adicional para criar o banco de teste; as permissões do exemplo são apenas para `biblioteca`.

### Proteção das credenciais

O `.gitignore` ignora `.env`, variantes privadas `.env.*`, `.venv`, `ll_env` e arquivos temporários, mas permite publicar `.env.example`. Esse modelo tem a senha vazia intencionalmente. O `.env` não criptografa nada: não o envie em prints, mensagens ou arquivos ZIP públicos.

Confira as regras com `git check-ignore -v .env`. Se `git ls-files .env` listar o arquivo, ele já está sendo acompanhado: execute `git rm --cached .env`, registre a remoção em um commit e publique esse commit. O arquivo continua no computador. Uma senha que já apareceu em um repositório precisa ser trocada; o comando não limpa versões antigas.

### Erros frequentes

| Mensagem | O que conferir |
|---|---|
| `No module named 'dotenv'` | Execute `python -m pip install -r requirements.txt` no mesmo ambiente do Django. |
| `No module named 'MySQLdb'` | Instale `requirements-mysql.txt` no ambiente ativo. |
| `Configuração MySQL incompleta` | Preencha os campos indicados e salve o `.env` ao lado de `manage.py`. |
| `Access denied ... (1045)` | Confira a conta MySQL, a senha e o host permitido. `using password: YES` só diz que uma senha foi enviada. |
| `Unknown database ... (1049)` | Crie o banco ou corrija `DB_NAME`; não use o nome do arquivo SQLite. |
| `Can't connect ... (2002/2003)` | Confira se o servidor está ativo e se host e porta estão corretos. |
| `DB_ENGINE deve ser mysql ou sqlite` | Corrija o nome do mecanismo no `.env` ou no ambiente. |

Se mudou o `.env` com o servidor aberto, pare e inicie `runserver` novamente. Não compartilhe senhas ao pedir ajuda.

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

Esta versão usa **um esquema novo em um único banco**, com o usuário padrão do Django. As migrations antigas (`usuarios`, `livros`, `emprestimos`, `escolas`) e os scripts SQL dos três bancos anteriores não são compatíveis com a nova migration inicial. **Não execute esta versão sobre um banco antigo com dados esperando que os dados sejam convertidos automaticamente.** Os arquivos antigos permanecem no histórico do Git; a documentação anterior indicava que os dumps fornecidos continham somente estrutura, mas confirme isso em qualquer instalação real antes de migrar. Faça backup, mapeie identificadores e relações, importe os dados em uma cópia e confira quantidades e empréstimos antes de trocar a instalação em uso.

O suporte ao MySQL já está configurado pelo `.env`, conforme o passo a passo. Executar `migrate` cria as tabelas, mas **não transfere** automaticamente os dados do SQLite ou dos três bancos antigos; planeje e teste a exportação/importação separadamente. Nunca coloque senhas no repositório.

## Limites desta versão

Ela foi feita para estudo e uso local inicial. Para colocar na internet, defina `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY` com uma chave privada e `DJANGO_ALLOWED_HOSTS` com os domínios separados por vírgulas no ambiente da hospedagem. Você pode gerar a chave localmente com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`; não publique o resultado. Sem DEBUG, a configuração exige uma chave; em estudo local, há uma chave de desenvolvimento como alternativa. Configure também HTTPS, backups e um servidor de aplicação adequado. Não use `runserver` como servidor público. Crie usuários de equipe pelo admin e marque **Membro da equipe** (`is_staff`); não existe cadastro público de administradores.
