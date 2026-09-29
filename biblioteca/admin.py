from django.contrib import admin

from .forms import LivroForm
from .models import Aluno, Emprestimo, Livro


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ["nome", "matricula", "turma"]
    search_fields = ["nome", "matricula"]


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    form = LivroForm
    list_display = ["titulo", "autor", "quantidade_total", "quantidade_disponivel"]
    search_fields = ["titulo", "autor"]
    fields = ["titulo", "autor", "editora", "categoria", "quantidade_total", "localizacao"]

    def save_model(self, request, obj, form, change):
        if change:
            antigo = Livro.objects.get(pk=obj.pk)
            obj.quantidade_disponivel = antigo.quantidade_disponivel + obj.quantidade_total - antigo.quantidade_total
        else:
            obj.quantidade_disponivel = obj.quantidade_total
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ["aluno", "livro", "data_emprestimo", "status"]
    list_filter = ["status"]
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
