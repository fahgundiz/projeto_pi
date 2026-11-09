from flask import render_template, request
from controllers.base_controller import BaseController

class FormularioController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/formulario', 'formulario', self.formulario),
            ('/formulario_resultado', 'formulario_resultado', self.formulario_resultado, ['POST'])
        ]
        
        super().__init__(app)

    def formulario(self):
        return render_template("formularios/formulario.html")

    def formulario_resultado(self):
        nome = request.form.get("nome")
        email = request.form.get("email")
        idade = request.form.get("idade")
        peso = request.form.get("peso")

        if not nome or not email or not idade or not peso:
            erro = "Preencha todos os campos obrigatórios"

        pessoa = {
            "nome":nome,
            "email":email,
            "idade":idade,
            "peso":peso
        }

        return render_template("formularios/formulario_resultado.html", pessoa = pessoa)
        