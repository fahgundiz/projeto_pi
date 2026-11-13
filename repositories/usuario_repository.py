
class UsuarioRepository:
    def __init__(self, banco):
        self.banco = banco

    def buscar_usuario_pelo_email(self, email):
        sql = """
            SELECT id, usuario, email, senha, data_nascimento, perfil
            FROM usuarios
            WHERE email = %s
"""
        usuario = self.banco.consultar_um(sql, (email,))

        return usuario