from database.connection import Banco
from services.usuario_service import UsuarioService

class Tabelas:
    def __init__(self, banco):
        self.banco = banco

    def criar_tabelas(self):
        self.criar_tabela_usuario()
        self.criar_tabela_logins()
        self.criar_tabela_ratelimit()
        self.criar_tabela_auditoria()

        self.criar_administrador()
        self.criar_usuario_teste()

        self.criar_tabela_exercicios()
        self.criar_tabela_treinos()
        self.criar_tabela_treino_exercicios()

        #desativar depois de roda 1 vez
        # self.inserir_dados_treino()


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
        sql = """
            CREATE TABLE IF NOT EXISTS auditoria (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NULL,
                acao VARCHAR(50) NOT NULL,
                entidade VARCHAR(50) NOT NULL,
                entidade_id INT NULL,
                ip VARCHAR(45),
                data_hora DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                ON DELETE SET NULL
            
            )
        """

        self.banco.executar(sql)

    def criar_tabela_exercicios(self):
        sql = """
            CREATE TABLE IF NOT EXISTS exercicios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE,
                grupo_muscular VARCHAR(50) NOT NULL,
                descricao TEXT
            )
        """
        self.banco.executar(sql)

    def criar_tabela_treinos(self):
        sql = """
            CREATE TABLE IF NOT EXISTS treinos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
"""
        self.banco.executar(sql)

    def criar_tabela_treino_exercicios(self):
        sql = """
            CREATE TABLE IF NOT EXISTS treino_exercicios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                treino_id INT NOT NULL,
                exercicio_id INT NOT NULL,
                series INT NOT NULL DEFAULT 3,
                repeticoes INT NOT NULL DEFAULT 10,
                carga_kg DECIMAL(6,2),
                descanso_seg INT DEFAULT 60,
                ordem INT NOT NULL DEFAULT 1,
                FOREIGN KEY (treino_id) REFERENCES treinos(id) ON DELETE CASCADE,
                FOREIGN KEY (exercicio_id) REFERENCES exercicios(id) ON DELETE RESTRICT
            )
"""
        self.banco.executar(sql)

    #===================== Teste para inserir dados para exercicio e treino =============
    def inserir_exercicios(self):
        exercicios = [
            ("Supino reto", "Peito"),
            ("Triceps testa", "Tríceps"),
            ("Agachamento livre", "Pernas")
        ]

        for nome, grupo in exercicios:
            sql = "INSERT INTO exercicios (nome, grupo_muscular) VALUES (%s, %s)"
            self.banco.executar(sql, (nome, grupo))
        print("Exercícios inseridos na tabela")

    def criar_treino(self):
        usuario_id = 1
        sql = "INSERT INTO treinos(usuario_id, nome, descricao) VALUES (%s, %s, %s)"
        self.banco.executar(sql, (usuario_id,"Treino A", "Peito e tríceps"))

    def inserir_exercicios_treino(self):
        supino = self.banco.consultar_um("SELECT id FROM exercicios WHERE nome = %s", ("Supino reto",))
        triceps = self.banco.consultar_um("SELECT id FROM exercicios WHERE nome = %s", ("Tríceps testa",))
        treino_id = 1

        self.banco.executar(
            """INSERT INTO treino_exercicios
            (treino_id, exercicio_id, series, repeticoes, carga_kg, ordem)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (treino_id, supino["id"], 4, 8, 60.0, 1)
        )
        
        self.banco.executar(
            """INSERT INTO treino_exercicios
            (treino_id, exercicio_id, series, repeticoes, carga_kg, ordem)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (treino_id, triceps["id"], 3, 12, 20.0, 2)
        )
        print("Itens adicionados ao treino")

    def inserir_dados_treino(self):
        self.inserir_exercicios()
        self.criar_treino()
        self.inserir_exercicios_treino()

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

    def criar_usuario_teste(self):

        existe_usuario = self.banco.consultar_um(
            """
                SELECT id FROM usuarios WHERE usuario = %s
            """,("teste",)
        )

        if not existe_usuario:
            #Criptografar a senha
            senha_hash = UsuarioService.gerar_hash_senha(senha = "123456")

            sql = """
                INSERT INTO usuarios (usuario, email, senha, data_nascimento, perfil)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.banco.executar(sql, ("teste", "teste@gmail.com", senha_hash, "1997-09-09", "usuario"))