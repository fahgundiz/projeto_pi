from controllers.base_controller import BaseController
from database.connection import Banco


from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

from flask import render_template, request, session, redirect, url_for

class UsuarioController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/exercicios', 'exercicios', self.exercicios, ['GET']),
            ('/exercicios/criar', 'criar_exercicio', self.criar_exercicio, ['GET','POST']),
            ('/treinos', 'treinos', self.treinos, ['GET']),
            ('/treinos/<int:treino_id>', 'treino_detalhe', self.treino_detalhe, ['GET']),

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

    def treinos(self):
        #Buscar o id do usuário para buscar todos os treinos do usuário
        usuario_id = session.get("usuario_id")

        
        #Busca todos os treinos do usuário logado
        treinos = self.usuario_service.listar_treinos(usuario_id)

        return render_template("treinos.html", treinos = treinos)

    def treino_detalhe(self, treino_id):
        usuario_id = session.get("usuario_id")
        
        try:
            treino, exercicios = self.usuario_service.detalhar_treino(treino_id, usuario_id)
        except ValueError:
            return redirect(url_for("treinos"))

        return render_template("treino_detalhe.html", treino = treino, exercicios=exercicios)
