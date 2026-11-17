from controllers.base_controller import BaseController
from database.connection import Banco


from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

from flask import render_template, request, session, redirect, url_for

class UsuarioController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/exercicios', 'exercicios', self.exercicios, ['GET','POST']),

        ]

        super().__init__(app)

        self.banco = Banco()

        self.usuario_repository = UsuarioRepository(self.banco)
        self.usuario_service = UsuarioService(self.usuario_repository)


    def exercicios(self):
        #Buscar a lista de exercícios
        exercicios = self.usuario_service.listar_exercicios()
        grupo = request.args.get("grupo", "").strip()

        return render_template("exercicios.html", exercicios = exercicios, grupo = grupo)