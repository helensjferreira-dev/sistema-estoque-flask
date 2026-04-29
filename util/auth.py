from functools import wraps
from flask import session, redirect, url_for

#Fechando as páginas para usuários logados

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("app_logon_realizado"):
            return redirect(url_for("usuario_routes.rota_usuario_login"))

        return f(*args, **kwargs)
    return decorated_function
