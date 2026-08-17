from django.db import models


class Escola(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=30, unique=True, help_text="Código interno/INEP ou outro identificador")
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome
