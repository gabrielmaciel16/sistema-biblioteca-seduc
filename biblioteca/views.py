from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import F, ProtectedError
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import AlunoForm, EmprestimoForm, LivroForm
from .models import Aluno, Emprestimo, Livro


@staff_member_required(login_url="login")
def inicio(request):
    return render(request, "inicio.html", {
        "alunos": Aluno.objects.count(),
        "livros": Livro.objects.count(),
        "ativos": Emprestimo.objects.filter(status=Emprestimo.Status.ATIVO).count(),
    })


@staff_member_required(login_url="login")
def alunos(request):
    return render(request, "alunos/lista.html", {"alunos": Aluno.objects.all()})


@staff_member_required(login_url="login")
def aluno_novo(request):
    formulario = AlunoForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        messages.success(request, "Aluno cadastrado.")
        return redirect("alunos")
    return render(request, "formulario.html", {"formulario": formulario, "titulo": "Cadastrar aluno", "voltar": "alunos"})


@staff_member_required(login_url="login")
def aluno_editar(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    formulario = AlunoForm(request.POST or None, instance=aluno)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        messages.success(request, "Aluno atualizado.")
        return redirect("alunos")
    return render(request, "formulario.html", {"formulario": formulario, "titulo": "Editar aluno", "voltar": "alunos"})


@staff_member_required(login_url="login")
def aluno_excluir(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == "POST":
        try:
            aluno.delete()
            messages.success(request, "Aluno excluído.")
        except ProtectedError:
            messages.error(request, "Este aluno tem empréstimos no histórico e não pode ser excluído.")
        return redirect("alunos")
    return render(request, "confirmar.html", {"objeto": aluno, "voltar": "alunos"})


@staff_member_required(login_url="login")
def livros(request):
    return render(request, "livros/lista.html", {"livros": Livro.objects.all()})


@staff_member_required(login_url="login")
def livro_novo(request):
    formulario = LivroForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        livro = formulario.save(commit=False)
        livro.quantidade_disponivel = livro.quantidade_total
        livro.save()
        messages.success(request, "Livro cadastrado.")
        return redirect("livros")
    return render(request, "formulario.html", {"formulario": formulario, "titulo": "Cadastrar livro", "voltar": "livros"})


@staff_member_required(login_url="login")
def livro_editar(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    formulario = LivroForm(request.POST or None, instance=livro)
    if request.method == "POST" and formulario.is_valid():
        with transaction.atomic():
            atual = Livro.objects.select_for_update().get(pk=pk)
            emprestados = atual.quantidade_total - atual.quantidade_disponivel
            if formulario.cleaned_data["quantidade_total"] < emprestados:
                formulario.add_error("quantidade_total", "O total não pode ser menor que os exemplares emprestados.")
            else:
                livro = formulario.save(commit=False)
                livro.quantidade_disponivel = livro.quantidade_total - emprestados
                livro.save()
                messages.success(request, "Livro atualizado.")
                return redirect("livros")
    return render(request, "formulario.html", {"formulario": formulario, "titulo": "Editar livro", "voltar": "livros"})


@staff_member_required(login_url="login")
def livro_excluir(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == "POST":
        try:
            livro.delete()
            messages.success(request, "Livro excluído.")
        except ProtectedError:
            messages.error(request, "Este livro tem empréstimos no histórico e não pode ser excluído.")
        return redirect("livros")
    return render(request, "confirmar.html", {"objeto": livro, "voltar": "livros"})


@staff_member_required(login_url="login")
def emprestimos_ativos(request):
    itens = Emprestimo.objects.filter(status=Emprestimo.Status.ATIVO).select_related("aluno", "livro")
    return render(request, "emprestimos/lista.html", {"itens": itens, "titulo": "Empréstimos ativos", "ativos": True, "hoje": timezone.localdate()})


@staff_member_required(login_url="login")
def emprestimo_novo(request):
    formulario = EmprestimoForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        livro = formulario.cleaned_data["livro"]
        with transaction.atomic():
            # O UPDATE condicional evita que dois pedidos consumam o último exemplar.
            alterados = Livro.objects.filter(pk=livro.pk, quantidade_disponivel__gt=0).update(
                quantidade_disponivel=F("quantidade_disponivel") - 1
            )
            if alterados:
                formulario.save()
                messages.success(request, "Empréstimo registrado.")
                return redirect("emprestimos_ativos")
        formulario.add_error("livro", "Este livro já não possui exemplares disponíveis.")
    return render(request, "formulario.html", {"formulario": formulario, "titulo": "Registrar empréstimo", "voltar": "emprestimos_ativos"})


@staff_member_required(login_url="login")
@require_POST
def devolver(request, pk):
    with transaction.atomic():
        emprestimo = get_object_or_404(Emprestimo, pk=pk)
        alterados = Emprestimo.objects.filter(pk=pk, status=Emprestimo.Status.ATIVO).update(
            status=Emprestimo.Status.DEVOLVIDO, data_devolucao=timezone.localdate()
        )
        if alterados:
            estoque_atualizado = Livro.objects.filter(pk=emprestimo.livro_id, quantidade_disponivel__lt=F("quantidade_total")).update(
                quantidade_disponivel=F("quantidade_disponivel") + 1
            )
            if not estoque_atualizado:
                raise ValueError("Estoque inconsistente: devolução não concluída.")
            messages.success(request, "Devolução registrada.")
        else:
            messages.warning(request, "Este empréstimo já foi devolvido.")
    return redirect("emprestimos_ativos")


@staff_member_required(login_url="login")
def historico(request):
    itens = Emprestimo.objects.select_related("aluno", "livro")
    return render(request, "emprestimos/lista.html", {"itens": itens, "titulo": "Histórico de empréstimos", "ativos": False, "hoje": timezone.localdate()})
