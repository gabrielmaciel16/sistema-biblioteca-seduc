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
        if self.instance.pk:
            anterior = Livro.objects.get(pk=self.instance.pk)
            emprestados = anterior.quantidade_total - anterior.quantidade_disponivel
            if total < emprestados:
                self.add_error("quantidade_total", "O total não pode ser menor que os exemplares emprestados.")
            else:
                self.instance.quantidade_disponivel = total - emprestados
        else:
            self.instance.quantidade_disponivel = total
        return dados


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ["aluno", "livro", "data_prevista_devolucao"]
        widgets = {"data_prevista_devolucao": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["livro"].queryset = Livro.objects.filter(quantidade_disponivel__gt=0)

    def clean_data_prevista_devolucao(self):
        data = self.cleaned_data["data_prevista_devolucao"]
        if data < timezone.localdate():
            raise forms.ValidationError("A previsão não pode estar no passado.")
        return data
