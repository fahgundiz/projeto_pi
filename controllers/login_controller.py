from controllers.base_controller import BaseController
from flask import render_template, request, session, redirect, url_for

class LoginController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/login', 'login', self.login),
            ('/entrar', 'entrar', self.entrar, ['POST']),
            ('/logout', 'logout', self.logout)
        ]

        super().__init__(app)

    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for('home'))

        return render_template("login/login.html")

    def entrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario_valido = {
            "email":"teste@gmail.com",
            "senha":"123456"
        }

        if email == usuario_valido["email"] and senha == usuario_valido["senha"]:
            session["usuario_logado"] = True
            session["email"] = email
            session["password"] = senha

            return redirect(url_for("home"))
        
        else:
            return render_template('login/login.html', erro = "E-mail ou senha incorretos")

    def logout(self):
        session.clear()
        return redirect(url_for("login"))