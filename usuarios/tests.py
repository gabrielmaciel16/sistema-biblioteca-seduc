from django.test import TestCase
from django.urls import reverse

from .models import User


class AutenticacaoTest(TestCase):
    def test_senha_fica_com_hash(self):
        user = User.objects.create_user(email="aluno@example.com", password="SenhaSegura123!")
        self.assertNotEqual(user.password, "SenhaSegura123!")
        self.assertTrue(user.check_password("SenhaSegura123!"))

    def test_dashboard_exige_login(self):
        response = self.client.get(reverse("usuarios:dashboard"))
        self.assertEqual(response.status_code, 302)
