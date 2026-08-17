from django.urls import path
from . import views

app_name = "emprestimos"
urlpatterns = [
    path("", views.meus_emprestimos, name="lista"),
]
