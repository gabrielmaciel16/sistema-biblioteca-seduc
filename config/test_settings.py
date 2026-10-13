"""Verifica a configuração sem acessar um servidor MySQL ou o .env real."""
import os
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured


class ConfiguracaoTests(TestCase):
    def carregar(self, conteudo="", ambiente=None):
        with TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / "config").mkdir()
            arquivo = raiz / "config" / "settings.py"
            arquivo.write_text(Path(__file__).with_name("settings.py").read_text(), encoding="utf-8")
            (raiz / ".env").write_text(conteudo, encoding="utf-8")
            with patch.dict(os.environ, ambiente or {}, clear=True):
                return runpy.run_path(str(arquivo))

    def test_sqlite_continua_disponivel_sem_credenciais(self):
        config = self.carregar()
        self.assertEqual(config["DATABASES"]["default"]["ENGINE"], "django.db.backends.sqlite3")
        self.assertEqual(config["DATABASES"]["default"]["NAME"], config["BASE_DIR"] / "db.sqlite3")

    def test_env_da_raiz_carrega_mysql_e_preserva_ambiente_externo(self):
        config = self.carregar(
            'DB_ENGINE=mysql\nDB_NAME=biblioteca\nDB_USER=aplicacao\n'
            'DB_PASSWORD="valor-ficticio#com-simbolo"\nDB_HOST=localhost\n',
            {"DB_HOST": "servidor-externo", "DB_PORT": "3307"},
        )
        banco = config["DATABASES"]["default"]
        self.assertEqual(banco["ENGINE"], "django.db.backends.mysql")
        self.assertEqual(banco["PASSWORD"], "valor-ficticio#com-simbolo")
        self.assertEqual((banco["HOST"], banco["PORT"]), ("servidor-externo", "3307"))

    def test_mysql_incompleto_falha_sem_expor_senha(self):
        with self.assertRaises(ImproperlyConfigured) as erro:
            self.carregar("DB_ENGINE=mysql\nDB_PASSWORD=valor-ficticio\n")
        self.assertIn("DB_NAME, DB_USER", str(erro.exception))
        self.assertNotIn("valor-ficticio", str(erro.exception))

    def test_engine_invalido_nao_seleciona_outro_banco_silenciosamente(self):
        with self.assertRaisesRegex(ImproperlyConfigured, "DB_ENGINE"):
            self.carregar("DB_ENGINE=mysqll\n")

    def test_producao_exige_chave_propria(self):
        with self.assertRaisesRegex(ImproperlyConfigured, "DJANGO_SECRET_KEY"):
            self.carregar("DJANGO_DEBUG=False\n")
        config = self.carregar(
            "DJANGO_DEBUG=False\nDJANGO_SECRET_KEY=chave-ficticia-de-teste\n"
            "DJANGO_ALLOWED_HOSTS=localhost, 127.0.0.1,\n"
        )
        self.assertFalse(config["DEBUG"])
        self.assertEqual(config["ALLOWED_HOSTS"], ["localhost", "127.0.0.1"])
