from flask import Flask, jsonify, request, render_template, Blueprint
from services.lote_services import *
import traceback
from models.lotes import Lote 
from util.auth import login_required


lote_routes = Blueprint('lote_routes', __name__)

@lote_routes.route('/lote', methods=['GET'], endpoint='pagina_lote')
@login_required
def pagina_lote():
    try:
        return render_template("lote.html")
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@lote_routes.route('/lote/lotes', methods=['GET', 'POST'])
def exibe_lotes():
    if request.method == 'GET':
        try:
            resultado, mensagem = listar_todos_lotes()
            return jsonify({"dados": resultado, "mensagem": mensagem})
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500

    elif request.method == 'POST':
        try:
            dados = request.get_json()
            idproduto = dados.get("idproduto")
            idfornecedor = dados.get("idfornecedor")
            data_cadastro = dados.get("data_cadastro")
            data_validade = dados.get("data_validade")
            numero = dados.get("numero")
            quantidade = dados.get("quantidade")

            lote = Lote(None, idproduto, idfornecedor,
                        data_cadastro, data_validade, numero, quantidade)

            resultado, mensagem = novo_lote(lote)

            if resultado:
                return jsonify({"Resultado": True, "Mensagem": mensagem})
            else:
                return jsonify({"Resultado": False, "Mensagem": mensagem})

        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500


@lote_routes.route('/lote/lote/<int:id>', methods=['GET'])
def get_lote(id):
    try:
        resultado, mensagem = buscar_lote_por_id(id)
        if resultado:
            return jsonify({"dados": resultado, "mensagem": mensagem})
        else:
            return jsonify({"Mensagem": mensagem}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


#Buscar lote por número (SEM DUPLICAR)
@lote_routes.route('/lote/buscar_por_numero_produto', methods=['GET'])
def buscar_lote_por_numero_produto_route():
    try:
        numero = request.args.get("numero")
        idproduto = request.args.get("idproduto")

        if not numero or not idproduto:
            return jsonify({"Mensagem": "numero e idproduto são obrigatórios"}), 400

        resultado, mensagem = buscar_lote_por_numero_e_produto(numero, idproduto)

        if not resultado:
            return jsonify({"Mensagem": mensagem}), 404

        return jsonify({"dados": resultado, "mensagem": mensagem})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@lote_routes.route('/lote/por-numero/<numero>', methods=['GET'])
def buscar_lote_por_numero_route(numero):
    try:
        # Busca lote apenas pelo número
        lote, mensagem = buscar_lote_por_numero(numero)

        if not lote:
            return jsonify({"Resultado": False, "Mensagem": mensagem, "dados": None}), 404

        # Buscar produto vinculado ao lote
        from services.produto_services import buscar_produto_por_id
        produto, _ = buscar_produto_por_id(lote["idproduto"])

        retorno = {
            "idlote": lote["idlote"],
            "idproduto": lote["idproduto"],
            "nome_produto": produto["nome"],
            "idcategoria": produto["idcategoria"],
        }

        return jsonify({"Resultado": True, "Mensagem": "OK", "dados": retorno})
    except Exception as e:
        return jsonify({"Resultado": False, "Mensagem": f"Erro: {e}", "dados": None}), 500



@lote_routes.route('/lote/fornecedor/<int:idfornecedor>', methods=['GET'])
def get_lote_fornecedor(idfornecedor):
    try:
        resultado, mensagem = buscar_lote_por_codigo_fornecedor(idfornecedor)
        if resultado:
            return jsonify({"dados": resultado, "mensagem": mensagem})
        else:
            return jsonify({"Mensagem": mensagem}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@lote_routes.route('/lote/produto/<int:idproduto>', methods=['GET'])
def get_lote_idproduto(idproduto):
    try:
        resultado, mensagem = buscar_lote_por_codigo_produto(idproduto)
        if resultado:
            return jsonify({"dados": resultado, "mensagem": mensagem})
        else:
            return jsonify({"Mensagem": mensagem}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@lote_routes.route('/lote/vencimento', methods=['GET'])
def get_lote_vencimento():
    try:
        data_validade_inicial = request.args.get("data_validade_inicial")
        data_validade_final = request.args.get("data_validade_final")

        resultado, mensagem = buscar_lote_por_vencimento(
            data_validade_inicial, data_validade_final)

        if resultado:
            return jsonify({"dados": resultado, "mensagem": mensagem})
        else:
            return jsonify({"Mensagem": mensagem}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@lote_routes.route('/lote/lote', methods=['PUT'])
def update_lote():
    try:
        dados = request.get_json()
        id = dados.get("id")
        idproduto = dados.get("idproduto")
        idfornecedor = dados.get("idfornecedor")
        data_cadastro = dados.get("data_cadastro")
        data_validade = dados.get("data_validade")
        numero = dados.get("numero")
        quantidade = dados.get("quantidade")

        lote = Lote(id, idproduto, idfornecedor,
                    data_cadastro, data_validade, numero, quantidade)

        resultado, mensagem = atualizar_lote(lote)

        if resultado:
            return jsonify({"Resultado": True, "Mensagem": mensagem})
        else:
            return jsonify({"Resultado": False, "Mensagem": mensagem})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@lote_routes.route('/lote/lote/<int:id>', methods=["DELETE"])
def rota_excluir_lote(id):
    dados = request.get_json(silent=True) or {}   # lê o body enviado pelo fetch
    idusuario = dados.get("idusuario")            # pega o idusuario

    resultado, mensagem = excluir_lote(id, idusuario)  # passa os dois argumentos, se necessário
    if resultado:
        return jsonify({"Resultado": True, "Mensagem": mensagem})
    else:
        return jsonify({"Resultado": False, "Mensagem": mensagem})


