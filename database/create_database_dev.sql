-- Banco único recomendado para o projeto Django (ambiente de desenvolvimento).
-- TROQUE a senha antes de executar.
CREATE DATABASE IF NOT EXISTS raiz_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'raiz_app'@'localhost'
  IDENTIFIED BY 'TROQUE_ESTA_SENHA';

-- Permissões limitadas ao banco da aplicação. Útil em desenvolvimento e migrations.
GRANT ALL PRIVILEGES ON raiz_db.* TO 'raiz_app'@'localhost';
FLUSH PRIVILEGES;
