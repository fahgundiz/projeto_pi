from database.connection import Banco
from services.usuario_service import UsuarioService

class Tabelas:
    def __init__(self, banco):
        self.banco = banco

    def criar_tabelas(self):
        self.criar_tabela_usuario()
        self.criar_tabela_logins()
        self.criar_tabela_ratelimit()

        self.criar_administrador()

    def criar_tabela_usuario(self):
        sql = """
            CREATE TABLE IF NOT EXISTS usuarios(
                id INT AUTO_INCREMENT PRIMARY KEY,

                usuario VARCHAR(255) UNIQUE NOT NULL,

                email VARCHAR(255) UNIQUE NOT NULL,

                senha VARCHAR(255) NOT NULL,

                data_nascimento DATE NOT NULL,

                perfil VARCHAR(50) NOT NULL DEFAULT 'usuario'
            )
"""
        self.banco.executar(sql)

    def criar_tabela_logins(self):
        sql = """
            CREATE TABLE IF NOT EXISTS logins (

                id INT AUTO_INCREMENT PRIMARY KEY,

                usuario_id INT NOT NULL,

                data_hora TIMESTAMP NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE
                
            )
"""
        self.banco.executar(sql)

    def criar_tabela_ratelimit(self):
        sql = """
            CREATE TABLE IF NOT EXISTS rate_limit (

                id INT AUTO_INCREMENT PRIMARY KEY,

                usuario_id INT NULL,

                ip VARCHAR(50) NOT NULL,

                rota VARCHAR(255) NOT NULL,

                metodo VARCHAR(10) NOT NULL,

                limite VARCHAR(50) NOT NULL,

                data_hora DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                motivo VARCHAR(255),

                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE SET NULL
            )
"""
        self.banco.executar(sql)

    def criar_tabela_auditoria(self):
        pass

    def criar_administrador(self):

        existe_usuario = self.banco.consultar_um(
            """
                SELECT id FROM usuarios WHERE usuario = %s
            """,("admin",)
        )

        if not existe_usuario:
            #Criptografar a senha
            senha_hash = UsuarioService.gerar_hash_senha(senha = "123456")

            sql = """
                INSERT INTO usuarios (usuario, email, senha, data_nascimento, perfil)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.banco.executar(sql, ("admin", "admin@gmail.com", senha_hash, "1997-09-09", "administrador"))