from django.test import TestCase
from .models import Escola


class EscolaModelTest(TestCase):
    def test_str_retorna_nome(self):
        escola = Escola(nome="Escola Teste", codigo="TESTE-001")
        self.assertEqual(str(escola), "Escola Teste")
