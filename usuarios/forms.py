from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import AlunoProfile, User


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "voce@email.com"}),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Sua senha"}),
    )


class CadastroAlunoForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150, required=False)
    email = forms.EmailField(label="E-mail")
    serie = forms.IntegerField(label="Série", min_value=1, max_value=9)
    curso = forms.CharField(label="Curso", max_length=50)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo = User.Tipo.ALUNO
        if commit:
            user.save()
            AlunoProfile.objects.create(
                user=user,
                serie=self.cleaned_data["serie"],
                curso=self.cleaned_data["curso"],
            )
        return user
