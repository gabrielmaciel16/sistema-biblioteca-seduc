from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import LoginForm
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "entrar/",
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("sair/", LogoutView.as_view(), name="logout"),
    path("cadastrar/", views.cadastro_aluno, name="cadastro"),
]
