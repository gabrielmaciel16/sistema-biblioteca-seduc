from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Livro


class LivroModelTest(TestCase):
    def test_disponivel_nao_pode_superar_total(self):
        livro = Livro(titulo="Teste", autor="Autor", quantidade_total=1, quantidade_disponivel=2)
        with self.assertRaises(ValidationError):
            livro.full_clean()
