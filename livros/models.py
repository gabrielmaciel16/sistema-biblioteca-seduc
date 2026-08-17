from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class Livro(models.Model):
    escola = models.ForeignKey(
        "escolas.Escola",
        on_delete=models.PROTECT,
        related_name="livros",
        null=True,
        blank=True,
        help_text="Durante o protótipo pode ficar vazio; em produção, associe cada livro a uma escola.",
    )
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    editora = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=50, blank=True)
    quantidade_total = models.PositiveIntegerField(default=1)
    quantidade_disponivel = models.PositiveIntegerField(default=1)
    localizacao = models.CharField(max_length=50, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["titulo", "autor"]
        constraints = [
            models.CheckConstraint(
                condition=Q(quantidade_disponivel__lte=F("quantidade_total")),
                name="livro_disponivel_nao_supera_total",
            )
        ]

    def clean(self):
        super().clean()
        if self.quantidade_disponivel > self.quantidade_total:
            raise ValidationError("A quantidade disponível não pode superar a quantidade total.")

    def __str__(self):
        return f"{self.titulo} — {self.autor}"
