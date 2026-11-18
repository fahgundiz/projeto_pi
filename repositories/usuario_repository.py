
class UsuarioRepository:
    def __init__(self, banco):
        self.banco = banco

    def buscar_usuario_pelo_email(self, email):
        """
        Busca um usuário pelo email dele e retorna o usuário.
        """
        sql = """
            SELECT id, usuario, email, senha, data_nascimento, perfil
            FROM usuarios
            WHERE email = %s
"""
        usuario = self.banco.consultar_um(sql, (email,))

        return usuario

    def existe_exercicio(self, nome):
        sql = "SELECT id FROM exercicios WHERE nome = %s"
        existe = self.banco.consultar_um(sql, (nome,))
        return existe
    
    def cadastrar_exercicio(self, nome, grupo_muscular, descricao = None):
        """
        Cadastra um exercício na tabela exercicios e devolve seu ID.
        """
        sql = """
            INSERT INTO exercicios (nome, grupo_muscular, descricao)
            VALUES (%s, %s, %s)
"""
        return self.banco.executar(sql, (nome, grupo_muscular, descricao))

    def listar_exercicios(self, grupo_muscular = None):
        sql = """
            SELECT
                id,
                nome,
                grupo_muscular,
                descricao

            FROM exercicios
            WHERE 1 = 1
        """

        parametros = []

        if grupo_muscular:
            sql += """
                AND grupo_muscular LIKE %s
            """
            parametros.append(f"%{grupo_muscular}%")

        sql += """ ORDER BY nome"""

        return self.banco.consultar(sql, tuple(parametros))