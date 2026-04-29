from conn import conectar
from models.produtos import Produto

from services.lote_services import listar_todos_lotes
 
from datetime import datetime


# Função auxiliar para padronizar controle_validade

def normalizar_controle_validade(valor):
    """
    Converte valores do banco ("S","N","1","0",True,False) 
    para boolean padronizado.
    """
    if valor in ("S", "1", 1, True):
        return True
    return False


# LISTAR TODOS OS PRODUTOS

def listar_todos_produtos():
    from services.categoria_services import buscar_categoria_por_id    

    comandoSQL = """
        SELECT 
            P.IDPRODUTO,
            P.IDCATEGORIA,
            P.NOME,
            P.DESCRICAO,
            P.CONTROLE_VALIDADE,
            P.ESTOQUE_MINIMO,
            COALESCE(SUM(
                CASE 
                    WHEN M.TIPO = 'entrada' THEN M.QUANTIDADE
                    WHEN M.TIPO = 'saida'   THEN -M.QUANTIDADE
                    ELSE 0
                END
            ), 0) AS ESTOQUE_ATUAL
        FROM PRODUTO P
        LEFT JOIN LOTE L 
            ON L.IDPRODUTO = P.IDPRODUTO
        LEFT JOIN MOVIMENTACAO M 
            ON M.IDLOTE = L.IDLOTE
        GROUP BY 
            P.IDPRODUTO, P.IDCATEGORIA, P.NOME, P.DESCRICAO, 
            P.CONTROLE_VALIDADE, P.ESTOQUE_MINIMO
        ORDER BY P.IDPRODUTO
    """

    resultado = []
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(comandoSQL)
        dados = cur.fetchall()

        for item in dados:
            produto = {
                "id": item[0],
                "idcategoria": item[1],
                "nome": item[2],
                "descricao": item[3],
                "controle_validade": normalizar_controle_validade(item[4]),
                "estoque_minimo": item[5],
                "estoque_atual": item[6]  # alias da soma das movimentações
            }

            categoria, _ = buscar_categoria_por_id(produto["idcategoria"])
            produto["categoria"] = categoria if categoria else {"id": None, "nome": "-"}

            resultado.append(produto)

        cur.close()
        con.close()
        return resultado, "OK"

    except Exception as e:
        print("Erro ao listar produtos:", e)
        return [], "Erro"


# BUSCAR POR ID

def buscar_produto_por_id(id):
    from services.categoria_services import buscar_categoria_por_id
    builder = Produto.get_SQLBuilder()
    sql, valores = builder.select_sql_and_values({"id": id})

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(sql, valores)
        dado = cur.fetchone()

        if dado:
            produto = Produto.from_db(dado).to_dict()

            #Normalizar controle_validade
            produto["controle_validade"] = normalizar_controle_validade(produto["controle_validade"])

            categoria, _ = buscar_categoria_por_id(produto["idcategoria"])
            produto["categoria"] = categoria["nome"] if categoria else None

            return produto, "OK"
        else:
            return None, "Produto não encontrado"

    except Exception as e:
        print("Erro ao buscar produto:", e)
        return None, "Erro"


# NOVO PRODUTO

def novo_produto(produto):
    resultado = False

    if isinstance(produto, Produto):
        try:
            builder = Produto.get_SQLBuilder()
            comandoSQL, valoresFiltro = builder.insert_sql_and_values(produto)

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute(comandoSQL, valoresFiltro)
            registrosAfetados = cursor.rowcount
            conexao.commit()

            cursor.close()
            conexao.close()

            resultado = True
            mensagem = f"Foram incluídos {registrosAfetados} registros"

        except Exception as e:
            resultado = False
            mensagem = "Erro ao incluir um novo produto"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = "Produto inválido"

    return resultado, mensagem


# ATUALIZAR PRODUTO

def atualizar_produto(produto):
    resultado = False

    if isinstance(produto, Produto):
        try:
            builder = Produto.get_SQLBuilder()
            comandoSQL, valoresFiltro = builder.update_sql_and_values(produto)

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute(comandoSQL, valoresFiltro)
            registrosAfetados = cursor.rowcount
            conexao.commit()

            cursor.close()
            conexao.close()

            resultado = True
            mensagem = f"Foram alterados {registrosAfetados} registros"

        except Exception as e:
            resultado = False
            mensagem = "Erro na atualização do produto"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = "Produto inválido"

    return resultado, mensagem


# EXCLUIR PRODUTO

def excluir_produto(id):
    builder = Produto.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.delete_sql_and_values(
        Produto(id, None, None, None, None, None)
    )

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL, valoresFiltro)
        registrosAfetados = cursor.rowcount
        conexao.commit()

        cursor.close()
        conexao.close()

        return True, f"Foram excluídos {registrosAfetados} registros"

    except Exception as e:
        print(f"Erro ao excluir o produto {id}: {e}")
        return False, "Erro ao excluir produto"


# LISTAR PRODUTOS POR CATEGORIA

def produto_lista_categoria(idcategoria):
    builder = Produto.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.select_sql_and_values({"idcategoria": idcategoria})

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL, valoresFiltro)
        dados = cursor.fetchall()
        registrosAfetados = cursor.rowcount

        if dados:
            resultado = []
            for item in dados:
                p = Produto.from_db(item).to_dict()
                p["controle_validade"] = normalizar_controle_validade(p["controle_validade"])
                resultado.append(p)
        else:
            resultado = None

        cursor.close()
        conexao.close()

        return resultado, f"Foram encontrados {registrosAfetados} registros"

    except Exception as e:
        print(f"Erro ao localizar produtos por categoria: {e}")
        return None, "Erro"


# LISTA ALERTA DE ESTOQUE

def produto_lista_alerta_estoque():
    comandoSQL = """
        SELECT IDPRODUTO, ESTOQUE_MINIMO, ESTOQUE, ALERTA_ESTOQUE, IDLOTE
        FROM VW_ESTOQUE
    """

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL)
        dados = cursor.fetchall()
        registrosAfetados = cursor.rowcount

        if dados:
            resultado = []
            for item in dados:
                resultado.append({
                    "idproduto": item[0],
                    "minimo": item[1],
                    "estoque": item[2],
                    "alerta": item[3],
                    "idlote": item[4]
                })
        else:
            resultado = None

        cursor.close()
        conexao.close()

        return resultado, f"Foram encontrados {registrosAfetados} registros"

    except Exception as e:
        print("Erro ao localizar alerta de estoque:", e)
        return None, "Erro"


# LISTA ALERTA DE VALIDADE

def produto_lista_alerta_validade():
    comandoSQL = """
        SELECT IDPRODUTO, IDLOTE, DATA_VALIDADE, DIAS_RESTANTES, ESTOQUE, ALERTA_VALIDADE
        FROM VW_VALIDADE
    """

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL)
        dados = cursor.fetchall()
        registrosAfetados = cursor.rowcount

        if dados:
            resultado = []
            for item in dados:
                data_validade_formatada = datetime.strftime(item[2], "%Y-%m-%d")
                resultado.append({
                    "idproduto": item[0],
                    "idlote": item[1],
                    "data_validade": data_validade_formatada,
                    "diasRestantes": item[3],
                    "estoque": item[4],
                    "alerta": item[5]
                })
        else:
            resultado = None

        cursor.close()
        conexao.close()

        return resultado, f"Foram encontrados {registrosAfetados} registros"

    except Exception as e:
        print("Erro ao localizar alerta de validade:", e)
        return None, "Erro"
