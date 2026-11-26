from functools import wraps
from flask import session, redirect, url_for, abort


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
            elif len(rota) == 5:
                endereco_url, nome_rota, funcao_resposta, metodos, perfil = rota
                funcao_protegida = self.proteger_rota(funcao_resposta, perfil)
                self.app.add_url_rule(endereco_url, nome_rota, funcao_protegida, methods = metodos)

    def proteger_rota(self, funcao_protegida, perfil=None):
        @wraps(funcao_protegida)
        def rota_protegida(*args, **kwargs):
            print("1. guarda acionado para:", funcao_protegida.__name__)
            print("2. logado?", session.get("usuario_logado"))
            print("3. perfil:", session.get("perfil_logado"), "| exigido:", perfil)
            if not session.get("usuario_logado"):
                return redirect(url_for("login"))
            if perfil is not None:
                if session.get("perfil_logado") != perfil:
                    abort(403)
            return funcao_protegida(*args, **kwargs)
        return rota_protegida