from flask import Flask, jsonify, request, render_template, Blueprint, session
from werkzeug.security import generate_password_hash, check_password_hash

from services.usuario_services import *
import traceback
from util.auth import login_required


usuario_routes=Blueprint('usuario_routes', __name__)

@usuario_routes.route('/usuario', methods=['GET'], endpoint='pagina_usuario')
#Rota ajustada para aceitar barra /
@usuario_routes.route('/usuario/', methods=["GET"], endpoint='pagina_usuario_barra')
@login_required
def pagina_usuario():
    try:
        return render_template("users.html")
        
    except Exception as e:
        return jsonify({"erro":str(e)}),500

@usuario_routes.route('/usuario/usuarios', methods=['GET','POST'])

def exibe_todos_usuarios():
    if request.method == 'GET':
        try:
            resultado, mensagem = listar_todos_usuarios()
            return jsonify({"dados":resultado, "mensagem":mensagem})
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500

    elif request.method == 'POST':
        try:
            dados = request.get_json()
            nome = dados.get("nome")
            email = dados.get("email")
            senha = dados.get("senha")
#escondendo a senha do usuario
            senha_hash = generate_password_hash(senha)

            usuario = Usuario(None, nome, email, senha_hash)
            resultado, mensagem = novo_usuario(usuario)

            if resultado:
#Padronizando o retorno JSON
                return jsonify({"Resultado":True, "Mensagem":mensagem})
            else:
                return jsonify({"Resultado":False, "Mensagem":mensagem})

        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500
    
@usuario_routes.route('/usuario/usuario/<int:id>', methods=['GET'])
def get_usuario_por_id(id):
    try:

        resultado, mensagem = buscar_usuario_por_id(id)
        if resultado:
            return jsonify({"dados":resultado, "mensagem":mensagem})
        else:
            return jsonify({"Mensagem":mensagem})

    except Exception as e:
        return jsonify({"erro":str(e)}),500

   
@usuario_routes.route('/usuario/usuario',methods=['PUT']) 
def update_usuario():
    try:
        dados=request.get_json()
        id = dados.get("id")
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")
        # escondendo a senha do usuario 
        senha_hash = generate_password_hash(senha)

        usuario = Usuario(id, nome, email, senha_hash)
        resultado, mensagem = alterar_usuario(usuario)

        if resultado:
            return jsonify({"Resultado":True, "Mensagem":mensagem})
        else:
            return jsonify({"Resultado":False, "Mensagem":mensagem})


    except Exception as e:
        return jsonify({"erro":str(e)}),500

@usuario_routes.route('/usuario/usuario/<int:id>', methods=["DELETE"])
def rota_excluir_usuario(id):
    resultado, mensagem = excluir_usuario(id)
    if resultado:
        return jsonify({"Resultado":True, "Mensagem":mensagem})
    else:
        return jsonify({"Resultado":False, "Mensagem":mensagem})
    

@usuario_routes.route('/usuario/login', methods=["GET"], endpoint='rota_usuario_login')
def rota_usuario_login():
    return render_template("login.html")

#rota para validar usuario e senha
@usuario_routes.route('/usuario/logon', methods=["POST"])
def rota_usuario_logon():
    dados = request.get_json()
    email = dados.get("email")
    senha = dados.get("senha")

    usuario = usuario_login(email)

    if usuario and check_password_hash(usuario.senha, senha):
        session["usuario"] = usuario.nome
        session["idusuario"] = usuario.id
        session["app_logon_realizado"] = True
        print("Sessão após login:", dict(session))
        return jsonify({"Resultado":True, "Mensagem":"Login realizado com sucesso"})


    else:
        session.clear()
        #Retornando 401 para falha de login
        return jsonify({"Resultado": False,"Mensagem":"Usuário e senha inválidos"}), 401


#rota para remover a sessão do usuario
@usuario_routes.route('/usuario/logoff', methods=["GET"])
def rota_usuario_logoff():
    session.clear()  #Limpa toda a sessão
    return jsonify([{"Resultado": True, "Mensagem": "Sessão finalizada com sucesso"}])