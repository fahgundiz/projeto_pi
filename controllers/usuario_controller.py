from controllers.base_controller import BaseController
from database.connection import Banco


from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

from flask import render_template, request, session, redirect, url_for

class UsuarioController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/exercicios', 'exercicios', self.proteger_rota(self.exercicios), ['GET']),
            ('/exercicios/criar', 'criar_exercicio', self.proteger_rota(self.criar_exercicio), ['GET','POST']),
            ('/treinos', 'treinos', self.proteger_rota(self.treinos), ['GET']),
            ('/treinos/novo', 'treino_novo', self.proteger_rota(self.treino_novo), ['GET', 'POST']),
            ('/treinos/<int:treino_id>', 'treino_detalhe', self.proteger_rota(self.treino_detalhe), ['GET']),

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

    def treino_novo(self):
        #busca o ID do usuário
        usuario_id = session.get("usuario_id")

        #Busca os exercícios cadastrados
        catalogo = self.usuario_service.listar_exercicios()

        #Se for requisição GET só retorna a página
        if request.method == "GET":   
            return render_template("treino_novo.html", catalogo = catalogo)

        #Se for POST, busca os campos
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()

        #Busca as listas com os ids, series, reps, cargas e descansos
        ids = request.form.getlist("exercicio_id")
        series = request.form.getlist("series")
        reps = request.form.getlist("repeticoes")
        cargas = request.form.getlist("carga_kg")
        descansos = request.form.getlist("descanso_seg")

        #Criar a lista de dicionários
        itens = []
        for i in range(len(ids)):
            if not ids[i]:
                continue
            itens.append({
                "exercicio_id": int(ids[i]),
                "series":int(series[i]),
                "repeticoes": int(reps[i]),
                "carga_kg":float(cargas[i]) if cargas[i] else None,
                "descanso_seg":int(descansos[i]) if descansos[i] else None,
            })
        try:
            treino_id = self.usuario_service.criar_treino(usuario_id, nome, descricao or None, itens)

        except ValueError as e:
            return render_template("treino_novo.html", catalogo = catalogo, erro = str(e), nome = nome, descricao = descricao)

        return redirect(url_for("treino_detalhe", treino_id = treino_id))