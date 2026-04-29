from flask import Flask, jsonify, request, render_template, Blueprint

from services.produto_services import *
import traceback

from models.produtos import Produto
from util.auth import login_required


produto_routes=Blueprint('produto_routes', __name__)

@produto_routes.route('/produto', methods=["GET"], endpoint='pagina_produto')
#Rota ajustada para aceitar barra /
@produto_routes.route('/produto/', methods=["GET"], endpoint='pagina_produto_barra')
@login_required
def pagina_produto():
    return render_template("produtos.html")


@produto_routes.route('/produto/produtos', methods=['GET','POST'])

def exibe_produtos():
    if request.method == 'GET':
        try:
            resultado, mensagem = listar_todos_produtos()
            return jsonify({"dados":resultado, "mensagem":mensagem})
        
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500

    elif request.method == 'POST':
        try:
            dados = request.get_json()
            idcategoria = dados.get("idcategoria")
            nome = dados.get("nome")
            descricao = dados.get("descricao")
            controle_validade = dados.get("controle_validade")
            estoque_minimo = dados.get("estoque_minimo")
            produto = Produto(None, idcategoria, nome, descricao, controle_validade, estoque_minimo) 
            resultado, mensagem = novo_produto(produto)

            if resultado:
                return jsonify({"Resultado": True, "Mensagem": mensagem})
            else:
                return jsonify({"Resultado": False, "Mensagem": mensagem})
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500
    

@produto_routes.route('/produto/produto/<int:id>', methods=['GET'])
def get_produto(id):
    try:
        resultado, mensagem=buscar_produto_por_id(id)
        if resultado:
            return jsonify({"dados":resultado, "mensagem":mensagem})
        else:
            #Retornar 404 se não encontrar
            return jsonify({"Mensagem":mensagem}), 404 

    except Exception as e:
        return jsonify({"erro":str(e)}),500

@produto_routes.route('/produto/produto',methods=['PUT'])
def update_produto():
    try:
        dados=request.get_json()
        id = dados.get("id")
        idcategoria = dados.get("idcategoria")
        nome = dados.get("nome")
        descricao = dados.get("descricao")
        controle_validade = dados.get("controle_validade")
        estoque_minimo = dados.get("estoque_minimo")
        produto = Produto(id, idcategoria, nome, descricao, controle_validade, estoque_minimo)
        resultado, mensagem = atualizar_produto(produto)

        if resultado:
            return jsonify({"Resultado": True, "Mensagem": mensagem})
        else:
            return jsonify({"Resultado": False, "Mensagem": mensagem})
    except Exception as e:
        return jsonify({"erro":str(e)}),500


@produto_routes.route('/produto/produto/<int:id>', methods=["DELETE"])
def delete_produto(id):
    resultado, mensagem = excluir_produto(id)
    if resultado:
        return jsonify({"Resultado": True, "Mensagem": mensagem})
    else:
        return jsonify({"Resultado": False, "Mensagem": mensagem})

@produto_routes.route('/produto/alerta_estoque', methods=["GET"])
def rota_listar_produto_alerta_estoque():
    resultado, mensagem = produto_lista_alerta_estoque()
    if resultado:
        return jsonify({"dados":resultado, "mensagem":mensagem})
    else:
        #Retornar 404 se não houver alerta
        return jsonify({"Mensagem":mensagem}), 404 
@produto_routes.route('/produto/alerta_validade', methods=["GET"])
def rota_listar_produto_alerta_validade():
    resultado, mensagem = produto_lista_alerta_validade()
    if resultado:
        return jsonify({"dados":resultado, "mensagem":mensagem})
    else:
        #Retornar 404 se não houver alerta
        return jsonify({"Mensagem":mensagem}), 404