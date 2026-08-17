from django.contrib import admin
from .models import Escola


@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo", "ativa")
    search_fields = ("nome", "codigo")
    list_filter = ("ativa",)
