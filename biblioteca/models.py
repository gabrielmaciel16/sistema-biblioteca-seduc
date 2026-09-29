from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class Aluno(models.Model):
    nome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=30, unique=True)
    turma = models.CharField(max_length=50)
    curso = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.matricula})"


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    editora = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=80, blank=True)
    quantidade_total = models.PositiveIntegerField(default=1)
    quantidade_disponivel = models.PositiveIntegerField(default=1)
    localizacao = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["titulo", "autor"]
        constraints = [models.CheckConstraint(
            condition=Q(quantidade_disponivel__lte=F("quantidade_total")),
            name="disponivel_ate_total",
        )]

    def clean(self):
        if self.quantidade_disponivel > self.quantidade_total:
            raise ValidationError("A quantidade disponível não pode superar a quantidade total.")

    def __str__(self):
        return f"{self.titulo} — {self.autor}"


class Emprestimo(models.Model):
    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        DEVOLVIDO = "DEVOLVIDO", "Devolvido"

    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, related_name="emprestimos")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="emprestimos")
    data_emprestimo = models.DateField(default=timezone.localdate)
    data_prevista_devolucao = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ATIVO)

    class Meta:
        ordering = ["-data_emprestimo", "-id"]
        constraints = [models.CheckConstraint(
            condition=(Q(status="ATIVO", data_devolucao__isnull=True)
                       | Q(status="DEVOLVIDO", data_devolucao__isnull=False)),
            name="status_conforme_devolucao",
        )]

    def __str__(self):
        return f"{self.aluno} — {self.livro}"
