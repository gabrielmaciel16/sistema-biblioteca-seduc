from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("tipo", User.Tipo.SUPERADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Tipo(models.TextChoices):
        ALUNO = "ALUNO", "Aluno"
        FUNCIONARIO = "FUNCIONARIO", "Funcionário"
        ADMIN_ESCOLA = "ADMIN_ESCOLA", "Administrador da escola"
        SUPERADMIN = "SUPERADMIN", "Administrador geral"

    username = None
    email = models.EmailField("e-mail", unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.ALUNO)
    escola = models.ForeignKey(
        "escolas.Escola",
        on_delete=models.PROTECT,
        related_name="usuarios",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.get_full_name() or self.email


class AlunoProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="aluno_profile")
    serie = models.PositiveSmallIntegerField()
    curso = models.CharField(max_length=50)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.serie}ª série"
