from controllers.base_controller import BaseController
from database.connection import Banco

from repositories.login_repository import LoginRepository
from services.login_service import LoginService

from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

from flask import render_template, request, session, redirect, url_for

class LoginController(BaseController):
    def __init__(self, app):
        self.rotas = [
            ('/login', 'login', self.login),
            ('/entrar', 'entrar', self.entrar, ['POST']),
            ('/logout', 'logout', self.logout)
        ]

        super().__init__(app)

        self.banco = Banco()
        self.login_repository = LoginRepository(self.banco)
        self.login_service = LoginService(self.login_repository)

        self.usuario_repository = UsuarioRepository(self.banco)
        self.usuario_service = UsuarioService(self.usuario_repository)


    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for('home'))

        return render_template("login/login.html")

    def entrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        #Buscar o usuário pelo E-mail (Dicionário de dados do usuário)
        usuario = self.usuario_service.buscar_usuario_pelo_email(email)

        usuario_id = usuario["id"]
        usuario_senha = usuario["senha"]

        senha_correta_ou_falsa = self.usuario_service.verificar_senha(senha, usuario_senha)

        if email == usuario["email"] and senha_correta_ou_falsa:
            session["usuario_logado"] = True
            session["email"] = email
            session["password"] = senha

            #Registrar login na tabela logins
            self.login_service.registrar_login(usuario_id)

            return redirect(url_for("home"))
        
        else:
            return render_template('login/login.html', erro = "E-mail ou senha incorretos")

    def logout(self):
        session.clear()
        return redirect(url_for("login"))