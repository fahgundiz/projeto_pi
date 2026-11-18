from controllers.base_controller import BaseController
from database.connection import Banco


from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

from flask import render_template, request, session, redirect, url_for

class UsuarioController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/exercicios', 'exercicios', self.exercicios, ['GET']),
            ('/criar_exercicio', 'criar_exercicio', self.criar_exercicio, ['GET','POST']),

        ]

        super().__init__(app)

        self.banco = Banco()

        self.usuario_repository = UsuarioRepository(self.banco)
        self.usuario_service = UsuarioService(self.usuario_repository)


    def exercicios(self):
        #Buscar a lista de exercícios
        grupo = request.args.get("grupo", "").strip()

        exercicios = self.usuario_service.listar_exercicios(grupo or None)
        

        return render_template("exercicios.html", exercicios = exercicios, grupo = grupo)

    def criar_exercicio(self):
        #Se acessar pela primeira vez
        if request.method == "GET":
            return render_template("criar_exercicio.html")

        #Se for POST, buscar os campos 
        nome = request.form.get("nome")
        grupo_muscular = request.form.get("grupo_muscular")
        descricao = request.form.get("descricao")

        try:
            self.usuario_service.cadastrar_exercicio(nome, grupo_muscular, descricao)
        except ValueError as erro:
            return render_template("criar_exercicio.html", erro = str(erro), nome = nome, grupo_muscular = grupo_muscular, descricao = descricao)

        return redirect(url_for('exercicios'))

