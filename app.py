from flask import Flask
from controllers.html_base_controller import HTMLBaseController


app = Flask(__name__)

#Registra as rotas
HTMLBaseController(app)

if __name__ == "__main__":
    app.run(debug=True)
