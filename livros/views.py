from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Livro


@login_required
def lista_livros(request):
    livros = Livro.objects.select_related("escola")

    if not request.user.is_superuser and request.user.escola_id:
        livros = livros.filter(escola=request.user.escola)

    termo = request.GET.get("q", "").strip()
    if termo:
        livros = livros.filter(Q(titulo__icontains=termo) | Q(autor__icontains=termo))

    return render(request, "livros/lista.html", {"livros": livros, "termo": termo})
