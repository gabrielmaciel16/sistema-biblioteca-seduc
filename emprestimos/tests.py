from django.test import TestCase

from escolas.models import Escola
from livros.models import Livro
from usuarios.models import User
from .models import Emprestimo
from .services import registrar_devolucao, registrar_emprestimo


class EmprestimoServiceTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(nome="Escola Teste", codigo="E-001")
        self.aluno = User.objects.create_user(
            email="aluno@example.com", password="SenhaSegura123!", tipo=User.Tipo.ALUNO, escola=self.escola
        )
        self.admin = User.objects.create_user(
            email="admin@example.com", password="SenhaSegura123!", tipo=User.Tipo.ADMIN_ESCOLA, escola=self.escola
        )
        self.livro = Livro.objects.create(
            escola=self.escola, titulo="Dom Casmurro", autor="Machado de Assis", quantidade_total=1, quantidade_disponivel=1
        )

    def test_emprestimo_reduz_disponibilidade_e_devolucao_restaura(self):
        emprestimo = registrar_emprestimo(aluno=self.aluno, livro_id=self.livro.id, registrado_por=self.admin)
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.quantidade_disponivel, 0)

        registrar_devolucao(emprestimo_id=emprestimo.id, registrado_por=self.admin)
        self.livro.refresh_from_db()
        emprestimo.refresh_from_db()
        self.assertEqual(self.livro.quantidade_disponivel, 1)
        self.assertEqual(emprestimo.status, Emprestimo.Status.DEVOLVIDO)
