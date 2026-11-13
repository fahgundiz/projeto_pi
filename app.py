from flask import Flask

from controllers.html_base_controller import HTMLBaseController
from controllers.login_controller import LoginController
from database.connection import Banco
from database.tables import Tabelas

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

limite = {
    "quantidade_requisicoes" : 5,
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


#Registra as rotas
HTMLBaseController(app)
LoginController(app)

if __name__ == "__main__":
    app.run(debug=True)


