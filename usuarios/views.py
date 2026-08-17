from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import CadastroAlunoForm


@transaction.atomic
def cadastro_aluno(request):
    if request.user.is_authenticated:
        return redirect("usuarios:dashboard")

    form = CadastroAlunoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("usuarios:dashboard")

    return render(request, "usuarios/cadastro.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "usuarios/dashboard.html")
