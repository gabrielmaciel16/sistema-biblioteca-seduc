from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("alunos/", views.alunos, name="alunos"),
    path("alunos/novo/", views.aluno_novo, name="aluno_novo"),
    path("alunos/<int:pk>/editar/", views.aluno_editar, name="aluno_editar"),
    path("alunos/<int:pk>/excluir/", views.aluno_excluir, name="aluno_excluir"),
    path("livros/", views.livros, name="livros"),
    path("livros/novo/", views.livro_novo, name="livro_novo"),
    path("livros/<int:pk>/editar/", views.livro_editar, name="livro_editar"),
    path("livros/<int:pk>/excluir/", views.livro_excluir, name="livro_excluir"),
    path("emprestimos/", views.emprestimos_ativos, name="emprestimos_ativos"),
    path("emprestimos/novo/", views.emprestimo_novo, name="emprestimo_novo"),
    path("emprestimos/<int:pk>/devolver/", views.devolver, name="devolver"),
    path("emprestimos/historico/", views.historico, name="historico"),
]
