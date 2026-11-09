from functools import wraps
from flask import session, redirect, url_for

#Antes de executar uma página, verifica se o usuário está logado
#Criando um decorador -> recebe a função que vai ser protegida
def login_required(funcao):
    #Wraps copia o nome e a descricao da funcao original
    @wraps(funcao)
    #Essa função vai substituir a original -> flexivel com args e kwargs
    def decorated_function(*args, **kwargs):
        #Verifica se o usuário está logado
        if not session.get("usuario_logado"):
            #Se nao estiver, redireciona para o login
            return redirect(url_for("login"))

        return funcao(*args, **kwargs)
    return decorated_function

#Cria a classe que serve de base para todos os controllers por herança
class BaseController:
    #Construtor que executa na hora que cria um objeto -> BaseController(app)
    def __init__(self, app):
        #Guarda o app dentro do objeto pra ser aproveitado pelas outras classes
        self.app = app
        #hasattr verifica se o objeto possui um atributo chamado 'rotas' -> toda classe que herda o base deve definir self.rotas
        if hasattr(self, 'rotas'):
            #Se possuir self.rotas -> registra todas elas no flask
            self.registrar_rotas()

    def registrar_rotas(self):
        #Percorre cada item da lista self.rotas definido na classe filha
        for rota in self.rotas:
            if len(rota) == 3:
                #Desempacota a tupla em 3 parametros: o caminho da URL, o nome interno da rota e a funcao executada
                endereco_url, nome_rota, funcao_resposta = rota
                #Registra a rota no flask é como usar o @app.route('/home') sobre a funcao
                self.app.add_url_rule(endereco_url, nome_rota, funcao_resposta)
            elif len(rota) == 4:
                endereco_url, nome_rota, funcao_resposta, metodos = rota
                self.app.add_url_rule(endereco_url,nome_rota, funcao_resposta, methods = metodos)

    def proteger_rota(self, funcao_protegida):
        return login_required(funcao_protegida)