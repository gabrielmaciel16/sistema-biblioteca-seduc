from django import forms
from django.utils import timezone

from .models import Aluno, Emprestimo, Livro


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "matricula", "turma", "curso", "telefone"]


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ["titulo", "autor", "editora", "categoria", "quantidade_total", "localizacao"]

    def clean(self):
        dados = super().clean()
        total = dados.get("quantidade_total")
        if total is None:
            return dados
        if total < 1:
            self.add_error("quantidade_total", "Informe pelo menos um exemplar.")

        emprestados = 0
        if self.instance.pk:
            emprestados = self.instance.quantidade_total - self.instance.quantidade_disponivel
        if total < emprestados:
            self.add_error("quantidade_total", "O total não pode ser menor que os exemplares emprestados.")
        else:
            # O formulário não mostra o estoque disponível; ele acompanha a mudança no total.
            self.instance.quantidade_disponivel = total - emprestados
        return dados


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ["aluno", "livro", "data_prevista_devolucao"]
        widgets = {"data_prevista_devolucao": forms.DateInput(attrs={"type": "date"})}

    def clean_data_prevista_devolucao(self):
        data = self.cleaned_data["data_prevista_devolucao"]
        if data < timezone.localdate():
            raise forms.ValidationError("A previsão não pode estar no passado.")
        return data
