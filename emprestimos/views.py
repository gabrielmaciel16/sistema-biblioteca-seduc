from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Emprestimo


@login_required
def meus_emprestimos(request):
    qs = Emprestimo.objects.select_related("livro", "aluno", "registrado_por")

    if request.user.tipo == "ALUNO":
        qs = qs.filter(aluno=request.user)
    elif not request.user.is_superuser and request.user.escola_id:
        qs = qs.filter(livro__escola=request.user.escola)

    return render(request, "emprestimos/lista.html", {"emprestimos": qs})
