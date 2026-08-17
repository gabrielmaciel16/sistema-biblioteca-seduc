from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Emprestimo(models.Model):
    class Status(models.TextChoices):
        ALUGADO = "ALUGADO", "Alugado"
        DEVOLVIDO = "DEVOLVIDO", "Devolvido"
        ATRASADO = "ATRASADO", "Atrasado"

    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="emprestimos",
        limit_choices_to={"tipo": "ALUNO"},
    )
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="emprestimos_registrados",
    )
    livro = models.ForeignKey("livros.Livro", on_delete=models.PROTECT, related_name="emprestimos")
    data_aluguel = models.DateField(default=timezone.localdate)
    data_prevista_devolucao = models.DateField(null=True, blank=True)
    data_devolucao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ALUGADO)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_aluguel", "-id"]

    def clean(self):
        super().clean()
        if self.aluno_id and self.aluno.tipo != "ALUNO":
            raise ValidationError({"aluno": "O usuário do empréstimo deve ser um aluno."})

        if self.aluno_id and self.livro_id:
            if self.aluno.escola_id and self.livro.escola_id and self.aluno.escola_id != self.livro.escola_id:
                raise ValidationError("Aluno e livro precisam pertencer à mesma escola.")

    def __str__(self):
        return f"{self.aluno} — {self.livro} ({self.get_status_display()})"
