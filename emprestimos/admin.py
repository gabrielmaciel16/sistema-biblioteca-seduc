from django.contrib import admin
from .models import Emprestimo


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "livro", "status", "data_aluguel", "data_prevista_devolucao", "data_devolucao", "registrado_por")
    list_filter = ("status", "livro__escola")
    search_fields = ("aluno__email", "aluno__first_name", "livro__titulo")
