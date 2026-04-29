from flask import Flask, jsonify, request, render_template, Blueprint
from services.fornecedor_services import *
from models.fornecedores import Fornecedor
import traceback
from util.auth import login_required


fornecedor_routes=Blueprint('fornecedor_routes', __name__)

@fornecedor_routes.route('/fornecedor', methods=["GET"], endpoint='pagina_fornecedor')
#Rota ajustada para aceitar barra /
@fornecedor_routes.route('/fornecedor/', methods=["GET"], endpoint='pagina_fornecedor_barra')
@login_required
def pagina_fornecedor():
    return render_template("fornecedor.html")


@fornecedor_routes.route('/fornecedor/fornecedores', methods=['GET','POST'])

def exibe_fornecedores():
    if request.method == 'GET':
        try:
            resultado, mensagem = listar_todos_fornecedores()
            return jsonify({"dados":resultado, "mensagem":mensagem})
        
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500

    elif request.method == 'POST':
        try:
            dados = request.get_json()

            nome = dados.get("nome")
            telefone = dados.get("telefone")
            email = dados.get("email")
            fornecedor = Fornecedor(None, nome, telefone, email)
            resultado, mensagem = novo_fornecedor(fornecedor)
            if resultado:
                return jsonify({"Resultado": True, "Mensagem": mensagem})
            else:
                return jsonify({"Resultado": False, "Mensagem": mensagem})

        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500
    
@fornecedor_routes.route('/fornecedor/fornecedor/<int:id>', methods=['GET'])
def get_fornecedor(id):
    try:
        resultado, mensagem=buscar_fornecedor_por_id(id)
        if resultado:
            return jsonify({"dados":resultado, "mensagem":mensagem})
        else:
            #Retorna 404 se não for encontrado
            return jsonify({"Mensagem":mensagem}), 404 

    except Exception as e:
        return jsonify({"erro":str(e)}),500

    
@fornecedor_routes.route('/fornecedor/fornecedor',methods=['PUT'])
def update_fornecedor():
    try:
        dados=request.get_json()
        id = dados.get("id")
        nome = dados.get("nome")
        telefone = dados.get("telefone")
        email = dados.get("email")
        fornecedor = Fornecedor(id, nome, telefone, email)
        resultado, mensagem = atualizar_fornecedor(fornecedor)
        if resultado:
            return jsonify({"Resultado": True, "Mensagem": mensagem})
        else:
            return jsonify({"Resultado": False, "Mensagem": mensagem})


    except Exception as e:
        return jsonify({"erro":str(e)}),500


@fornecedor_routes.route('/fornecedor/fornecedor/<int:id>', methods=["DELETE"])
def delete_fornecedor(id):
    resultado, mensagem = excluir_fornecedor(id)
    if resultado:
        return jsonify({"Resultado": True, "Mensagem": mensagem})
    else:
        return jsonify({"Resultado": False, "Mensagem": mensagem})