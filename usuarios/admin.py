from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AlunoProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "tipo", "escola", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("tipo", "escola", "is_active", "is_staff")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Dados pessoais", {"fields": ("first_name", "last_name", "tipo", "escola")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "tipo", "escola", "is_staff", "is_active"),
        }),
    )


@admin.register(AlunoProfile)
class AlunoProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "serie", "curso", "criado_em")
    search_fields = ("user__email", "user__first_name", "user__last_name", "curso")
