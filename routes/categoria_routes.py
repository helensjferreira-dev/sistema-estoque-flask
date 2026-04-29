from flask import Flask, jsonify, request, render_template, Blueprint
from flask_cors import CORS
from services.categoria_services import *
from util.auth import login_required
from models.categorias import Categoria 
import traceback

#Registro da rota
categoria_routes=Blueprint('categoria_routes', __name__)

@categoria_routes.route('/categoria', methods=["GET"], endpoint='pagina_categoria')
# Rota ajustada para aceitar barra /
@categoria_routes.route('/categoria/', methods=["GET"], endpoint='pagina_categoria_barra')
@login_required
def pagina_categoria():
    return render_template("categorias.html")
    

@categoria_routes.route('/categoria/categorias', methods=['GET','POST'])
def exibe_categorias():
    if request.method == 'GET':
        try:
            resultado, mensagem = listar_todas_categorias()
            return jsonify({"dados":resultado,"mensagem":mensagem})
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500

    elif request.method == 'POST':
        try:
            dados = request.get_json()
            nome = dados.get("nome")

            if not nome or nome.strip() == "":
                return jsonify({"Resultado": False, "Mensagem": "Nome da categoria é obrigatório"}), 400

            # Verificação de duplicidade
            todas, _ = listar_todas_categorias()
            existe = any(c["nome"].lower() == nome.lower() for c in todas)

            if existe:
                return jsonify({"Resultado": False, "Mensagem": "Categoria já existente."}), 400

            categoria = Categoria(None, nome)
            resultado, mensagem = nova_categoria(categoria)

            if resultado:
                return jsonify({"Resultado": True, "Mensagem": mensagem})
            else:
                return jsonify({"Resultado": False, "Mensagem": mensagem})
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500

    
@categoria_routes.route('/categoria/categoria/<int:id>', methods=['GET'])
def get_categoria(id):
    try:
        resultado, mensagem=buscar_categoria_por_id(id)
        if resultado:
            return jsonify({"dados":resultado, "mensagem":mensagem})
        else:
            # Retorna 404 se não encontrar
            return jsonify({"Mensagem":mensagem}), 404

    except Exception as e:
        return jsonify({"erro":str(e)}),500
    
@categoria_routes.route('/categoria/categoria',methods=['PUT'])
def update_categoria():
    try:
        dados = request.get_json()
        id = dados.get("id")
        nome = dados.get("nome")

        if existe_categoria_com_nome(nome, id_ignorar=id):
            return jsonify({"Resultado": False, "Mensagem": "Já existe outra categoria com esse nome."}), 400

        categoria = Categoria(id, nome)
        resultado, mensagem = atualizar_categoria(categoria)
        return jsonify({"Resultado": resultado, "Mensagem": mensagem})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@categoria_routes.route('/categoria/categoria/<int:id>', methods=["DELETE"])
def rota_categoria_excluir_existente(id):
    resultado, mensagem = excluir_categoria(id)
    if resultado:
        return jsonify({"Resultado": True, "Mensagem": mensagem})
    else:
        return jsonify({"Resultado": False, "Mensagem": mensagem})