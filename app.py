from flask import Flask
from controllers.html_base_controller import HTMLBaseController
from controllers.login_controller import LoginController


app = Flask(__name__)

app.secret_key = "chave_para_teste"
#Registra as rotas
HTMLBaseController(app)
LoginController(app)

if __name__ == "__main__":
    app.run(debug=True)
