from django.urls import path
from . import views

app_name = "livros"
urlpatterns = [
    path("", views.lista_livros, name="lista"),
]
