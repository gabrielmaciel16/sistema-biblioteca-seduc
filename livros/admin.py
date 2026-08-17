from django.contrib import admin
from .models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "escola", "quantidade_total", "quantidade_disponivel", "localizacao")
    search_fields = ("titulo", "autor", "editora", "categoria")
    list_filter = ("escola", "categoria")
