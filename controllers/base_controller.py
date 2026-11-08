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
            #Desempacota a tupla em 3 parametros: o caminho da URL, o nome interno da rota e a funcao executada
            endereco_url, nome_rota, funcao_resposta = rota
            #Registra a rota no flask é como usar o @app.route('/home') sobre a funcao
            self.app.add_url_rule(endereco_url, nome_rota, funcao_resposta)