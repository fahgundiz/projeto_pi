from controllers.base_controller import BaseController
from database.connection import Banco
from repositories.auditoria_repository import AuditoriaRepository
from services.auditoria_service import AuditoriaService
from flask import render_template


class AuditoriaController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/auditoria', 'auditoria', self.auditoria, ['GET'], "administrador"),
        ]
        super().__init__(app)

        self.banco = Banco()
        #Adicionar self.repository
        self.repository = AuditoriaRepository(self.banco)
        #Adicionar self.service
        self.service = AuditoriaService(self.repository)


    def auditoria(self):
        auditorias = self.service.listar_auditoria()
        
        return render_template("auditoria.html", auditorias = auditorias)