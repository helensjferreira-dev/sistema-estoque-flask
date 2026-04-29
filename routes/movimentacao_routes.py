from flask import jsonify, request, render_template, Blueprint, session
import traceback
from services import movimentacao_services
from models.movimentacoes import Movimentacao
from conn import conectar 
from util.auth import login_required


movimentacao_routes = Blueprint('movimentacao_routes', __name__)

@movimentacao_routes.route('/movimentacao', methods=['GET'])
@login_required
def pagina_movimentacoes():
    try:
        usuario_id = session.get('idusuario')
        usuario_nome = session.get('nome')
        return render_template("movimentacao.html", usuario_id=usuario_id, usuario_nome=usuario_nome)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# LISTAR / NOVA MOVIMENTAÇÃO

@movimentacao_routes.route('/movimentacao/movimentacoes', methods=['GET', 'POST'])
def exibe_movimentacoes():
    if request.method == 'GET':
        try:
            resultado, mensagem = movimentacao_services.listar_todas_movimentacoes()
            return jsonify({"dados": resultado, "mensagem": mensagem})
        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500

    else:  # POST
        try:
            dados = request.get_json() or {}
            idlote = dados.get("idlote")
            idusuario = dados.get("idusuario")
            idproduto = dados.get("idproduto")  
            data_movimentacao = dados.get("data_movimentacao")
            tipo = dados.get("tipo")
            quantidade = dados.get("quantidade")
            valor_unitario = dados.get("valor_unitario")
            motivo = dados.get("motivo")

            faltantes = [k for k, v in {
                "idlote": idlote,
                "idusuario": idusuario,
                "data_movimentacao": data_movimentacao,
                "tipo": tipo,
                "quantidade": quantidade
            }.items() if v in (None, "")]

            if faltantes:
                return jsonify({"Resultado": False, "Mensagem": f"Campos obrigatórios faltando: {', '.join(faltantes)}"}), 400

            #Validação lote/produto
            from services.lote_services import buscar_lote_por_id
            lote, _ = buscar_lote_por_id(idlote)
            if not lote:
                return jsonify({"Resultado": False, "Mensagem": "Lote inexistente."}), 400
            if str(lote["idproduto"]) != str(idproduto):
                return jsonify({"Resultado": False, "Mensagem": "O lote informado não pertence ao produto selecionado."}), 400

            movimentacao = Movimentacao(None, idlote, idusuario, data_movimentacao, tipo, quantidade, valor_unitario, motivo)
            resultado, mensagem = movimentacao_services.nova_movimentacao(movimentacao)
            status = 200 if resultado else 400

            if not resultado:
                return jsonify({"Resultado": False, "Mensagem": mensagem}), status

            #Buscar último ID inserido e retornar movimentação 
            from conn import conectar
            con = conectar()
            cur = con.cursor()
            cur.execute("SELECT MAX(IDMOVIMENTACAO) FROM MOVIMENTACAO")
            novo_id = cur.fetchone()[0]
            cur.close()
            con.close()

            mov, _ = movimentacao_services.buscar_movimentacoes_por_id(novo_id)
            return jsonify({"Resultado": True, "Mensagem": mensagem, "dados": mov}), 200

        except Exception as e:
            return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500


# BUSCAR POR ID

@movimentacao_routes.route('/movimentacao/movimentacao/<int:id>', methods=['GET'])
def get_movimentacao(id):
    try:
        resultado, mensagem = movimentacao_services.buscar_movimentacoes_por_id(id)
        if resultado:
            return jsonify({"dados": resultado, "mensagem": mensagem})
        else:
            return jsonify({"Mensagem": mensagem}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



# ATUALIZAR

@movimentacao_routes.route('/movimentacao/movimentacao', methods=['PUT'])
def update_movimentacao():
    try:
        dados = request.get_json() or {}
        idmov = dados.get("id") or dados.get("idmovimentacao")
        if not idmov:
            return jsonify({"Resultado": False, "Mensagem": "id da movimentação é obrigatório"}), 400

        movimentacao = Movimentacao(
            idmov,
            dados.get("idlote"),
            dados.get("idusuario"),
            dados.get("data_movimentacao"),
            dados.get("tipo"),
            dados.get("quantidade"),
            dados.get("valor_unitario"),
            dados.get("motivo")
        )
        resultado, mensagem = movimentacao_services.atualizar_movimentacao(movimentacao)
        status = 200 if resultado else 400
        return jsonify({"Resultado": resultado, "Mensagem": mensagem}), status
    except Exception as e:
        return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500



# EXCLUIR

@movimentacao_routes.route('/movimentacao/movimentacao/<int:id>', methods=['DELETE'])
def rota_excluir_movimentacao(id):
    try:
        resultado, mensagem = movimentacao_services.excluir_movimentacao(id)
        status = 200 if resultado else 400
        return jsonify({"Resultado": resultado, "Mensagem": mensagem}), status
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



# PESQUISA COM FILTROS

@movimentacao_routes.route('/movimentacao/pesquisa', methods=['GET'])
def rota_movimentacao_listar_filtros():
    try:
        args = request.args
        filtro = []
        valores = []

        def add(cond, val):
            filtro.append(cond)
            valores.append(val)

        if args.get("idproduto"):
            add("P.IDPRODUTO = %s", args.get("idproduto"))
        if args.get("idcategoria"):
            add("P.IDCATEGORIA = %s", args.get("idcategoria"))
        if args.get("idlote"):
            add("M.IDLOTE = %s", args.get("idlote"))
        if args.get("idmovimentacao"):
            add("M.IDMOVIMENTACAO = %s", args.get("idmovimentacao"))
        if args.get("tipo"):
            add("M.TIPO = %s", args.get("tipo"))
        if args.get("idfornecedor"):
            add("L.IDFORNECEDOR = %s", args.get("idfornecedor"))
        if args.get("idusuario"):
            add("M.IDUSUARIO = %s", args.get("idusuario"))
        if args.get("data_inicial") and args.get("data_final"):
            add("M.DATA_MOVIMENTOCAO >= %s", args.get("data_inicial"))
            add("M.DATA_MOVIMENTOCAO <= %s", args.get("data_final"))

        resultado, mensagem = movimentacao_services.movimentacao_listar_filtros(filtro, valores)
        if resultado:
            return jsonify({"dados": resultado, "mensagem": mensagem})
        else:
            return jsonify({"Mensagem": "Nenhum registro encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e), "trace": traceback.format_exc()}), 500
