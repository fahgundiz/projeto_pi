from controllers.base_controller import BaseController
from flask import render_template

#Cria a classe herdando o BaseController -> ganhando o registrar_rotas()
class HTMLBaseController(BaseController):
    def __init__(self, app):
        #Cria o atributo rotas -> ('a URL', 'nome do endpoint', 'a funcao que será executada')
        self.rotas = [
            ('/', 'home', self.home)
        ]
        #inicia a classe mãe (BaseController)
        #self.rotas precisa vir antes , pois o hasattr retornaria false e nao registraria rotas se fosse criado dps
        super().__init__(app)

    def home(self):
        return render_template('home.html')