from controllers.base_controller import BaseController
from database.connection import Banco

from repositories.login_repository import LoginRepository
from services.login_service import LoginService

from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

from repositories.auditoria_repository import AuditoriaRepository
from services.auditoria_service import AuditoriaService

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

        self.auditoria_repository = AuditoriaRepository(self.banco)
        self.auditoria_service = AuditoriaService(self.auditoria_repository)

    def login(self):
        if session.get("usuario_logado"):
            return redirect(url_for('home'))

        return render_template("login/login.html")

    def entrar(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        #Buscar o usuário pelo E-mail (Dicionário de dados do usuário)
        usuario = self.usuario_service.buscar_usuario_pelo_email(email)

        if not usuario:
            return render_template('login/login.html', erro = "E-mail ou senha incorretos")

        usuario_id = usuario["id"]
        usuario_senha = usuario["senha"]
        usuario_perfil = usuario["perfil"]

        senha_correta_ou_falsa = self.usuario_service.verificar_senha(senha, usuario_senha)

        if email == usuario["email"] and senha_correta_ou_falsa:
            session["usuario_id"] = usuario_id
            session["usuario_logado"] = True
            session["email"] = email
            session["perfil_logado"] = usuario_perfil

            #Registrar login na tabela logins
            self.login_service.registrar_login(usuario_id)

            #Registra o login na tabela auditoria
            self.auditoria_service.registrar_auditoria(usuario_id=usuario_id, acao="Login sucesso", entidade="Login", descricao="Login realizado com sucesso",ip=request.remote_addr)

            return redirect(url_for("home"))
        
        else:
            #Registrar o login falho na tabela auditoria
            self.auditoria_service.registrar_auditoria(usuario_id = None, acao="Login falha", entidade="Login", descricao="Login erro por e-mail ou senha incorretas", ip=request.remote_addr)
            return render_template('login/login.html', erro = "E-mail ou senha incorretos")

    def logout(self):
        session.clear()
        return redirect(url_for("login"))