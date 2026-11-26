from controllers.base_controller import BaseController
from database.connection import Banco
from flask import render_template


class AuditoriaController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/auditoria', 'auditoria', self.auditoria, ['GET'], "administrador"),
        ]
        super().__init__(app)

        self.banco = Banco()
        #Adicionar self.repository

        #Adicionar self.service

    def auditoria(self):
        return render_template("auditoria.html")