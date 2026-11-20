class RateLimitRepository:
    def __init__(self, banco):
        self.banco = banco


    def registrar_ratelimit(self, usuario_id = None, ip=None, rota = None, metodo = None, limite = None, motivo = None):
        sql = """
            INSERT INTO rate_limit (usuario_id, ip, rota, metodo, limite, motivo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        parametros = (usuario_id, ip, rota, metodo, limite, motivo)
        self.banco.executar(sql, parametros)

