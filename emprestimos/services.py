from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from livros.models import Livro
from usuarios.models import User
from .models import Emprestimo


@transaction.atomic
def registrar_emprestimo(*, aluno: User, livro_id: int, registrado_por: User, data_prevista_devolucao=None) -> Emprestimo:
    if aluno.tipo != User.Tipo.ALUNO:
        raise ValidationError("Apenas alunos podem receber empréstimos.")

    if registrado_por.tipo not in {User.Tipo.FUNCIONARIO, User.Tipo.ADMIN_ESCOLA, User.Tipo.SUPERADMIN} and not registrado_por.is_superuser:
        raise PermissionDenied("Este usuário não pode registrar empréstimos.")

    livro = Livro.objects.select_for_update().get(pk=livro_id)

    if aluno.escola_id and livro.escola_id and aluno.escola_id != livro.escola_id:
        raise PermissionDenied("Não é permitido emprestar livros de outra escola.")

    if livro.quantidade_disponivel < 1:
        raise ValidationError("Este livro não possui exemplares disponíveis.")

    emprestimo = Emprestimo.objects.create(
        aluno=aluno,
        registrado_por=registrado_por,
        livro=livro,
        data_prevista_devolucao=data_prevista_devolucao,
    )

    livro.quantidade_disponivel -= 1
    livro.save(update_fields=["quantidade_disponivel"])
    return emprestimo


@transaction.atomic
def registrar_devolucao(*, emprestimo_id: int, registrado_por: User) -> Emprestimo:
    if registrado_por.tipo not in {User.Tipo.FUNCIONARIO, User.Tipo.ADMIN_ESCOLA, User.Tipo.SUPERADMIN} and not registrado_por.is_superuser:
        raise PermissionDenied("Este usuário não pode registrar devoluções.")

    emprestimo = (
        Emprestimo.objects.select_for_update()
        .select_related("livro")
        .get(pk=emprestimo_id)
    )

    if emprestimo.status == Emprestimo.Status.DEVOLVIDO:
        raise ValidationError("Este empréstimo já foi devolvido.")

    livro = Livro.objects.select_for_update().get(pk=emprestimo.livro_id)
    livro.quantidade_disponivel = min(livro.quantidade_disponivel + 1, livro.quantidade_total)
    livro.save(update_fields=["quantidade_disponivel"])

    emprestimo.status = Emprestimo.Status.DEVOLVIDO
    emprestimo.data_devolucao = timezone.localdate()
    emprestimo.save(update_fields=["status", "data_devolucao"])
    return emprestimo
