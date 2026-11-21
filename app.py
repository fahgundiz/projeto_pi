from flask import Flask, session, render_template, request

from controllers.html_base_controller import HTMLBaseController
from controllers.login_controller import LoginController
from controllers.usuario_controller import UsuarioController
from database.connection import Banco
from database.tables import Tabelas

from repositories.ratelimit_repository import RateLimitRepository
from services.ratelimit_service import RateLimitService

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

limite = {
    "quantidade_requisicoes" : 100,
    "periodo" : "minute"
}

#adiciona limite de requisições
limiter = Limiter(
    key_func = get_remote_address, #identifica quem está fazendo a requisição -> get_remote_address extrai o IP do cliente
    app = app,
    default_limits = [f" {limite['quantidade_requisicoes']} per {limite['periodo']}"], #define regras para todas as rotas
    storage_uri ="memory://" #guarda o número de requisições no servidor
)

app.secret_key = "chave_para_teste"


#cria a instância do banco
banco = Banco()
#cria a instancia da tabela
tabelas = Tabelas(banco)
#Cria as tabelas do banco
tabelas.criar_tabelas()

ratelimit_repository = RateLimitRepository(banco)
ratelimit_service = RateLimitService(ratelimit_repository)

#Decorador vincula o erro HTTP 429 (Too many requests) a função abaixo
#Quando o flask limiter bloquear uma requisição, a função de baixo vai ser chamada
@app.errorhandler(429)
def limite_excedido(e): #O parametro "e" recebe o erro gerado
    ratelimit_service.registrar_ratelimit(
        usuario_id= session.get("usuario_id"), #Busca o ID do usuário logado, caso não esteja retorna None
        ip= request.remote_addr, #Pega o endereço IP de quem fez a requisição
        rota=request.path, #Busca o caminho da URL acessada
        metodo = request.method, #Captura o verbo HTTP utilizado ("GET" OU "POST")
        limite= str(e.description), #Extrai do objeto de erro 'e' a descrição da regra violada
        motivo = "Limite de tentativas excedido"
    )

    return render_template("login/login.html", erro = "Muitas tentativas. Aguarde um momento e tente novamente"), 429



#Registra as rotas
HTMLBaseController(app)
LoginController(app)
UsuarioController(app)

if __name__ == "__main__":
    app.run(debug=True)


