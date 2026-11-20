class RateLimitService:
    def __init__(self, repository):
        self.repository = repository

    def registrar_ratelimit(self, usuario_id = None, ip=None, rota = None, metodo = None, limite = None, motivo = None):
        self.repository.registrar_ratelimit(usuario_id = usuario_id, ip = ip, rota = rota, metodo = metodo, limite = limite, motivo = motivo)