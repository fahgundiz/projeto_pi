from functools import wraps
from flask import redirect, url_for, session, abort


def proteger_rota(self, funcao_protegida, perfil = None):
    @wraps(funcao_protegida)
    def rota_protegida(*args, **kwargs):
        if not session.get("usuario_logado"):
            return redirect(url_for("login"))
        if perfil is not None:
            if session.get("perfil_logado") != perfil:
                abort(403)
        return funcao_protegida(*args, **kwargs)
    return rota_protegida

