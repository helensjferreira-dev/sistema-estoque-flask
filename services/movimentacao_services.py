from conn import conectar
from datetime import datetime
from models.movimentacoes import Movimentacao

# Converter valores em int
def _to_int(value, field="valor"):
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
            return int(float(value))
        return int(value)
    except Exception:
        raise ValueError(f"{field} inválido: {value!r}")
    

# LISTAR TODAS AS MOVIMENTAÇÕES

def listar_todas_movimentacoes():
    comandoSQL = """
        SELECT 
            M.IDMOVIMENTACAO,      -- 0
            M.IDLOTE,              -- 1
            L.IDPRODUTO,           -- 2
            P.NOME AS NOME_PRODUTO, -- 3
            P.IDCATEGORIA,         -- 4
            C.NOME AS NOME_CATEGORIA, -- 5
            M.IDUSUARIO,           -- 6
            U.NOME AS NOME_USUARIO, -- 7
            M.MOTIVO,              -- 8
            M.QUANTIDADE,          -- 9
            M.VALOR_UNITARIO,      -- 10
            M.DATA_MOVIMENTOCAO,   -- 11
            M.TIPO                 -- 12
        FROM MOVIMENTACAO M
        JOIN LOTE L ON L.IDLOTE = M.IDLOTE
        JOIN PRODUTO P ON P.IDPRODUTO = L.IDPRODUTO
        LEFT JOIN CATEGORIA C ON C.IDCATEGORIA = P.IDCATEGORIA
        JOIN USUARIO U ON U.IDUSUARIO = M.IDUSUARIO
        ORDER BY M.IDMOVIMENTACAO DESC
    """

    resultado = []
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL)
        dados = cursor.fetchall()

        for item in dados:
            resultado.append({
                "idmovimentacao": item[0],
                "idlote": item[1],
                "idproduto": item[2],
                "nome_produto": item[3],
                "idcategoria": item[4],
                "nome_categoria": item[5],
                "idusuario": item[6],
                "nome_usuario": item[7],
                "motivo": item[8],
                "quantidade": item[9],
                "valor_unitario": float(item[10]) if item[10] else None,
                "data_movimentacao": item[11].strftime("%Y-%m-%d") if item[11] else None,
                "tipo": item[12]
            })

        cursor.close()
        conexao.close()
        mensagem = f"Foram encontrados {len(resultado)} registros"

    except Exception as e:
        print("ERRO GERAL AO LISTAR MOVIMENTAÇÕES:", e)
        resultado = []
        mensagem = "Erro ao listar as movimentações"

    return resultado, mensagem



# BUSCAR POR ID

def buscar_movimentacoes_por_id(id):
    comandoSQL = """
        SELECT 
            M.IDMOVIMENTACAO,
            M.IDLOTE,
            L.NUMERO AS numero_lote,
            L.IDPRODUTO,
            P.NOME AS NOME_PRODUTO,
            P.IDCATEGORIA,
            C.NOME AS NOME_CATEGORIA,
            M.IDUSUARIO,
            U.NOME AS NOME_USUARIO,
            M.MOTIVO,
            M.QUANTIDADE,
            M.VALOR_UNITARIO,
            M.DATA_MOVIMENTOCAO,
            M.TIPO
        FROM MOVIMENTACAO M
        JOIN LOTE L ON L.IDLOTE = M.IDLOTE
        JOIN PRODUTO P ON P.IDPRODUTO = L.IDPRODUTO
        LEFT JOIN CATEGORIA C ON C.IDCATEGORIA = P.IDCATEGORIA
        JOIN USUARIO U ON U.IDUSUARIO = M.IDUSUARIO
        WHERE M.IDMOVIMENTACAO = %s
    """

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL, (id,))
        item = cursor.fetchone()

        if item:
            resultado = {
                "idmovimentacao": item[0],
                "idlote": item[1],
                "numero_lote": item[2],
                "idproduto": item[3],
                "nome_produto": item[4],
                "idcategoria": item[5],
                "nome_categoria": item[6],
                "idusuario": item[7],
                "nome_usuario": item[8],
                "motivo": item[9],
                "quantidade": item[10],
                "valor_unitario": float(item[11]) if item[11] else None,
                "data_movimentacao": item[12].strftime("%Y-%m-%d") if item[12] else None,
                "tipo": item[13]
            }
        else:
            resultado = None

        cursor.close()
        conexao.close()
        return resultado, "OK"

    except Exception as e:
        print("ERRO AO BUSCAR POR ID:", e)
        return None, "Erro ao buscar movimentação"



# NOVA MOVIMENTAÇÃO

def nova_movimentacao(movimentacao):
    if not isinstance(movimentacao, Movimentacao):
        return False, "Movimentação inválida"

    try:
        tipo = (movimentacao.tipo or "").strip().lower()
        qtd = _to_int(movimentacao.quantidade, "quantidade")

        if qtd <= 0:
            return False, "Quantidade deve ser maior que zero."

        conexao = conectar()
        cursor = conexao.cursor()

        # Verifica quantidade atual do lote
        cursor.execute("SELECT quantidade FROM LOTE WHERE idlote = %s", (movimentacao.idlote,))
        row = cursor.fetchone()
        if not row:
            cursor.close(); conexao.close()
            return False, "Lote não encontrado."

        estoque_lote = _to_int(row[0], "estoque_lote")

        if tipo == "saida" and qtd > estoque_lote:
            cursor.close(); conexao.close()
            return False, f"Quantidade solicitada ({qtd}) maior que o estoque disponível no lote ({estoque_lote})."

        # Insere movimentação
        builder = Movimentacao.get_SQLBuilder()
        comandoSQL, valores = builder.insert_sql_and_values(movimentacao)
        cursor.execute(comandoSQL, valores)

        # Atualiza lote
        if tipo == "entrada":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade + %s WHERE idlote = %s", (qtd, movimentacao.idlote))
        elif tipo == "saida":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade - %s WHERE idlote = %s", (qtd, movimentacao.idlote))
        else:
            cursor.close(); conexao.close()
            return False, "Tipo de movimentação inválido. Use 'entrada' ou 'saida'."

        conexao.commit()
        cursor.close(); conexao.close()
        return True, "Movimentação registrada com sucesso"

    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        print("ERRO AO INSERIR MOV:", e)
        return False, "Erro ao registrar movimentação"


# ATUALIZAR

def atualizar_movimentacao(movimentacao):
    if not isinstance(movimentacao, Movimentacao):
        return False, "Movimentação inválida"

    try:
        tipo_novo = (movimentacao.tipo or "").strip().lower()
        qtd_nova = _to_int(movimentacao.quantidade, "quantidade")

        if qtd_nova <= 0:
            return False, "Quantidade deve ser maior que zero."

        conexao = conectar()
        cursor = conexao.cursor()

        # Busca movimentação antiga
        cursor.execute("SELECT idlote, tipo, quantidade FROM MOVIMENTACAO WHERE idmovimentacao = %s", (movimentacao.id,))
        mov_antiga = cursor.fetchone()
        if not mov_antiga:
            cursor.close(); conexao.close()
            return False, "Movimentação não encontrada"

        idlote_antigo, tipo_antigo, qtd_antiga = mov_antiga
        tipo_antigo = (tipo_antigo or "").strip().lower()
        qtd_antiga = _to_int(qtd_antiga, "quantidade antiga")

        # Reverte efeito antigo no lote
        if tipo_antigo == "entrada":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade - %s WHERE idlote = %s", (qtd_antiga, idlote_antigo))
        elif tipo_antigo == "saida":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade + %s WHERE idlote = %s", (qtd_antiga, idlote_antigo))

        # Estoque após reversão
        cursor.execute("SELECT quantidade FROM LOTE WHERE idlote = %s", (movimentacao.idlote,))
        estoque_atual = _to_int(cursor.fetchone()[0], "estoque")

        if tipo_novo == "saida" and qtd_nova > estoque_atual:
            conexao.rollback()
            cursor.close(); conexao.close()
            return False, f"Quantidade solicitada ({qtd_nova}) maior que o estoque disponível ({estoque_atual})."

        # Atualiza movimentação
        builder = Movimentacao.get_SQLBuilder()
        comandoSQL, valores = builder.update_sql_and_values(movimentacao)
        cursor.execute(comandoSQL, valores)

        # Aplica efeito novo no lote
        if tipo_novo == "entrada":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade + %s WHERE idlote = %s", (qtd_nova, movimentacao.idlote))
        elif tipo_novo == "saida":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade - %s WHERE idlote = %s", (qtd_nova, movimentacao.idlote))
        else:
            conexao.rollback()
            cursor.close(); conexao.close()
            return False, "Tipo de movimentação inválido. Use 'entrada' ou 'saida'."

        conexao.commit()
        cursor.close(); conexao.close()
        return True, "Movimentação atualizada com sucesso e estoque ajustado"

    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        print("ERRO AO ATUALIZAR MOV:", e)
        return False, "Erro ao atualizar movimentação"




# EXCLUIR

def excluir_movimentacao(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Buscar movimentação antes de excluir
        cursor.execute("SELECT idlote, tipo, quantidade FROM MOVIMENTACAO WHERE idmovimentacao = %s", (id,))
        mov = cursor.fetchone()
        if not mov:
            cursor.close()
            conexao.close()
            return False, "Movimentação não encontrada"

        idlote, tipo, quantidade = mov
        tipo = (tipo or "").strip().lower()
        quantidade = int(quantidade)

        # Reverter estoque no lote
        if tipo == "entrada":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade - %s WHERE idlote = %s", (quantidade, idlote))
        elif tipo == "saida":
            cursor.execute("UPDATE LOTE SET quantidade = quantidade + %s WHERE idlote = %s", (quantidade, idlote))

        # Excluir movimentação
        cursor.execute("DELETE FROM MOVIMENTACAO WHERE idmovimentacao = %s", (id,))
        conexao.commit()

        cursor.close()
        conexao.close()
        return True, "Movimentação excluída e estoque ajustado"

    except Exception as e:
        print("ERRO AO EXCLUIR:", e)
        return False, "Erro ao excluir movimentação"
