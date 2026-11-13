class LoginRepository:
    def __init__(self, banco):
        self.banco = banco

    def registrar_login(self, usuario_id):
        sql = """
            INSERT INTO logins (usuario_id)
            VALUES (%s)
"""
        self.banco.executar(sql, (usuario_id,))