from datetime import timedelta

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Aluno, Emprestimo, Livro


class BibliotecaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser("bibliotecario", "teste@escola.com", "senha-segura-123")
        self.client.force_login(self.usuario)
        self.aluno = Aluno.objects.create(nome="Ana", matricula="123", turma="2A")
        self.livro = Livro.objects.create(titulo="Livro de teste", autor="Autor", quantidade_total=1, quantidade_disponivel=1)
        self.data = (timezone.localdate() + timedelta(days=7)).isoformat()

    def emprestar(self):
        return self.client.post(reverse("emprestimo_novo"), {
            "aluno": self.aluno.pk, "livro": self.livro.pk,
            "data_prevista_devolucao": self.data,
        })

    def test_emprestimo_e_devolucao_atualizam_estoque_uma_vez(self):
        self.assertRedirects(self.emprestar(), reverse("emprestimos_ativos"))
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.quantidade_disponivel, 0)
        self.assertEqual(Emprestimo.objects.count(), 1)

        resposta = self.emprestar()
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Emprestimo.objects.count(), 1)

        emprestimo = Emprestimo.objects.get()
        url = reverse("devolver", args=[emprestimo.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.post(url)
        self.client.post(url)
        emprestimo.refresh_from_db()
        self.livro.refresh_from_db()
        self.assertEqual(emprestimo.status, Emprestimo.Status.DEVOLVIDO)
        self.assertEqual(emprestimo.data_devolucao, timezone.localdate())
        self.assertEqual(self.livro.quantidade_disponivel, 1)
        self.assertContains(self.client.get(reverse("historico")), "Devolvido")

    def test_editar_quantidade_preserva_exemplares_emprestados(self):
        self.emprestar()
        dados = {"titulo": self.livro.titulo, "autor": self.livro.autor,
                 "editora": "", "categoria": "", "localizacao": "", "quantidade_total": 3}
        self.assertRedirects(self.client.post(reverse("livro_editar", args=[self.livro.pk]), dados), reverse("livros"))
        self.livro.refresh_from_db()
        self.assertEqual((self.livro.quantidade_total, self.livro.quantidade_disponivel), (3, 2))
        dados["quantidade_total"] = 0
        self.assertEqual(self.client.post(reverse("livro_editar", args=[self.livro.pk]), dados).status_code, 200)
        self.livro.refresh_from_db()
        self.assertEqual((self.livro.quantidade_total, self.livro.quantidade_disponivel), (3, 2))
        self.client.post(reverse("devolver", args=[Emprestimo.objects.get().pk]))
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.quantidade_disponivel, 3)

    def test_protege_historico_e_exige_login(self):
        self.emprestar()
        self.client.post(reverse("aluno_excluir", args=[self.aluno.pk]))
        self.client.post(reverse("livro_excluir", args=[self.livro.pk]))
        self.assertTrue(Aluno.objects.filter(pk=self.aluno.pk).exists())
        self.assertTrue(Livro.objects.filter(pk=self.livro.pk).exists())
        self.client.logout()
        self.assertEqual(self.client.get(reverse("alunos")).status_code, 302)
        self.assertEqual(self.client.post(reverse("devolver", args=[Emprestimo.objects.get().pk])).status_code, 302)
        visitante = User.objects.create_user("visitante", password="senha-123")
        self.client.force_login(visitante)
        self.assertEqual(self.client.get(reverse("livros")).status_code, 302)

    def test_banco_impede_estoque_invalido(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Livro.objects.filter(pk=self.livro.pk).update(quantidade_disponivel=2)
