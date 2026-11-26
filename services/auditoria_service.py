class AuditoriaService:
    def __init__(self, repository):
        self.repository = repository

    def registrar_auditoria(self,usuario_id, acao, entidade, entidade_id = None, descricao = None, ip = None):
        self.repository.registrar_auditoria(usuario_id = usuario_id, acao = acao, entidade = entidade, entidade_id = entidade_id, descricao = descricao, ip = ip)

    def listar_auditoria(self, usuario_id = None, acao = None, entidade = None):
        return self.repository.listar_auditoria(usuario_id = usuario_id, acao = acao , entidade = entidade)