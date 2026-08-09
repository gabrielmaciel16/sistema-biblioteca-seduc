SEMPRE TRABALHAR COM BRANCHS
•Main:versão funcional do projeto, versão final do projeto
•Branch: versão paralela que não afeta o projeto principal 


•Como funcionará na prática o site?

HTML básico
→ páginas, títulos, formulários, botões, tabelas

 CSS básico
→ cores, tamanho, Flexbox, Grid, responsividade

JavaScript básico
→ variáveis, funções, eventos, DOM

 JavaScript + APIs
→ fetch(), JSON, requisições HTTP

Flask
→ criar a API do sistema

 MySQL
→ armazenar usuários, livros, empréstimos etc.






•Guia de aprendizado
Aprender HTML básico
       ↓
Criar primeira tela
       ↓
Aprender CSS necessário
       ↓
Melhorar a tela
       ↓
Aprender JS necessário
       ↓
Fazer a tela funcionar
       ↓
Aprender Flask
       ↓
Conectar ao banco



•Requisições do Front-End e Back-End

Usuário solicita livro
        ↓
Frontend envia solicitação
        ↓
Backend recebe
        ↓
Backend verifica banco
        ↓
Banco informa se disponível
        ↓
Backend responde
        ↓
Frontend mostra resultado




•Funcionamento da Hospedagem do site

Nosso computador 
       ↓
GitHub
       ↓
Servidor
       ↓
Site acessível pela internet



•Guia de como fazer,alterar e enviar alterações 

   [GitHub main]
1-criar umabranch
2-(Programar/testar)
3-commit
4-push
5-Pull Request
6-outra pessoa revisa
7-MERGE
8-main

•Proteção da Main através de configuração do Github 
Pessoa
   ↓
Branch
   ↓
Pull Request
   ↓
Review
   ↓
Testes
   ↓
MERGE



•Padronização de Commits 
Ex:
feat: adiciona cadastro de livros

fix: corrige erro na busca de livros

docs: atualiza documentação da API

refactor: reorganiza sistema de usuários

test: adiciona testes para login








•Funcionalidades básicas do GitHub para mexer no projeto
•Code:Código do projeto                         
•Issues Tarefas, bugs e problemas                 
•Pull Requests:Revisar código antes de entrar no projeto 
•Projects:Quadro geral do desenvolvimento           
•Actions:Automatizar testes futuramente 
•Wiki/Docs:Documentação, se necessário               
•Settings:Configurações e permissões             







Combinação Front-End
•Css:aparência 
•Html:estrutura do site
•Javascript:para interações e
Requisições de comunicação entre o Front-End e a API 


•Python
Python recebe a requisição do javascript e depois consulta o banco de dados MySQL que devolve os livros

Python não é um framework e precisa de um oara comunicação web

Flask e Django(ferramentas para usar Python na criação de aplicações web/API)

•Django:é mais completo e com mais recursos 
•Flask: é mais fácil e deixa mais evidente a intercalação entre as linguagens







•Versões futuras

•Fase 1 -MVP/Beta
Login
   ↓
Cadastro de livros
   ↓
Pesquisa de livros
   ↓
Empréstimo
   ↓
Devolução

•Fase 2
Painel administrativo
Estatísticas
Histórico
Filtros
Controle de estoque

•Fase 3
Múltiplas escolas
Perfis de usuários
Relatórios
Notificações

•Fase 4
Segurança avançada
Escalabilidade
Cloud
CI/CD
Monitoramento
Aplicativo mobile
