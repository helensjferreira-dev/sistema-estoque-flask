
from conn import conectar
from models.lotes import Lote


def listar_todos_lotes():

    builder = Lote.get_SQLBuilder()
    comandoSQL = builder.build_select()

    resultado=[]
    try:
        conexao=conectar()
        cursor=conexao.cursor() 
        cursor.execute(comandoSQL)
        dados=cursor.fetchall()
        registrosAfetados = cursor.rowcount        

        if dados:
            resultado=[Lote.from_db(item).to_dict() for item in dados]
        else:
            resultado = []
        cursor.close()
        conexao.close()

        mensagem = f"Foram encontrados {registrosAfetados} registros"
    except Exception as e:
        mensagem = f"Erro ao localizar os lotes de produtos"
        print(f"{mensagem} ({e})")
    
    return resultado, mensagem

def buscar_lote_por_id(id):
    builder = Lote.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.select_sql_and_values({"id": id})

    try: 
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(comandoSQL, valoresFiltro)
        dados = cursor.fetchone()
        registrosAfetados = cursor.rowcount
        # pegando os dados do banco e convertendo para objeto
        if dados:
            resultado = Lote.from_db(dados).to_dict()
        else:
            resultado = None

        cursor.close()
        conexao.close()

        mensagem = f"Foram encontrados {registrosAfetados} registros"
        return resultado, mensagem
    except Exception as e:
        print(f"Erro ao localizar o lote de produto {id}# {e}")
        print(f"{mensagem} ({e})")
        return None, mensagem

def buscar_lote_por_numero(numero):
    try:
        from models.lotes import Lote
        lote = Lote.buscar_por_numero(numero)  
        if lote:
            return lote, "Lote encontrado"
        else:
            return None, "Lote não encontrado"
    except Exception as e:
        return None, f"Erro: {e}"


def buscar_lote_por_numero_e_produto(numero, idproduto):
    sql = """
        SELECT IDLOTE, NUMERO, IDPRODUTO
        FROM LOTE
        WHERE NUMERO = %s AND IDPRODUTO = %s
        LIMIT 1
    """
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(sql, (numero, idproduto))
        row = cursor.fetchone()
        cursor.close()
        conexao.close()

        if row:
            #retorna dict simples
            return {"idlote": row[0], "numero": row[1], "idproduto": row[2]}, "OK"
        return None, "Nenhum lote encontrado para este produto"
    except Exception as e:
        print("Erro ao localizar lote:", e)
        return None, "Erro"



def buscar_lote_por_codigo_produto(idproduto):

    builder = Lote.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.select_sql_and_values({"idproduto": idproduto})

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(comandoSQL, valoresFiltro)
        dados = cursor.fetchall()
        registrosAfetados = cursor.rowcount   

        if dados:
            resultado = [Lote.from_db(item).to_dict() for item in dados]
        else:
            resultado = []
     
        cursor.close()
        conexao.close()

        mensagem = f"Foram encontrados {registrosAfetados} registros"
    except Exception as e:
        mensagem = f"Erro ao localizar os lotes de produtos"
        print(f"{mensagem} ({e})")
    
    return resultado, mensagem

def buscar_lote_por_codigo_fornecedor(idfornecedor):

    builder = Lote.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.select_sql_and_values({"idfornecedor": idfornecedor})

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(comandoSQL, valoresFiltro)
        dados = cursor.fetchall()
        registrosAfetados = cursor.rowcount 
        if dados:
            resultado = [Lote.from_db(item).to_dict() for item in dados]
        else:
            resultado = []

        cursor.close()
        conexao.close()

        mensagem = f"Foram encontrados {registrosAfetados} registros"
    except Exception as e:
        mensagem = f"Erro ao localizar os lotes de produtos"
        print(f"{mensagem} ({e})")
    
    return resultado, mensagem

#Listar por periodo de vencimento
def buscar_lote_por_vencimento(data_validade_inicial, data_validade_final):

    builder = Lote.get_SQLBuilder()
    
    #montando a consulta base de select sem where
    comandoSQL = builder.build_select(None)
    comandoSQL += " WHERE DATA_VALIDADE >= %s AND DATA_VALIDADE <= %s"    

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(comandoSQL, (data_validade_inicial, data_validade_final))
        dados = cursor.fetchall()
        registrosAfetados = cursor.rowcount
        if dados:
            resultado = [Lote.from_db(item).to_dict() for item in dados]
        else:
            resultado = []

        cursor.close()
        conexao.close()

        mensagem = f"Foram encontrados {registrosAfetados} registros"
    except Exception as e:
        mensagem = f"Erro ao localizar os lotes de produtos"
        print(f"{mensagem} ({e})")
    
    return resultado, mensagem

def novo_lote(lote):
    resultado = False

    if isinstance(lote, Lote):
        builder = Lote.get_SQLBuilder()
        comandoSQL, valoresFiltro = builder.insert_sql_and_values(lote)

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            # Inserir lote
            cursor.execute(comandoSQL, valoresFiltro)
            registrosAfetados = cursor.rowcount

            conexao.commit()
            cursor.close()
            conexao.close()

            resultado = True
            mensagem = f"Foram incluídos {registrosAfetados} registros de lote"

        except Exception as e:
            resultado = False
            mensagem = f"Erro ao incluir um novo lote de produto"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = f"Lote inválido"
        print(f"{mensagem}")
        
    return resultado, mensagem




#alterar um lote existente

def atualizar_lote(lote, idusuario, motivo="Ajuste de lote"):
    resultado = False
    if isinstance(lote, Lote):
        try:
            conexao = conectar()
            cursor = conexao.cursor()

            # Atualizar lote 
            builder = Lote.get_SQLBuilder()
            comandoSQL, valoresFiltro = builder.update_sql_and_values(lote)
            cursor.execute(comandoSQL, valoresFiltro)
            registrosAfetados = cursor.rowcount        

            conexao.commit()
            cursor.close()
            conexao.close()

            resultado = True
            mensagem = f"Foram alterados {registrosAfetados} registros"
        except Exception as e:
            resultado = False
            mensagem = f"Erro na atualização do lote de produto ({e})"
            print(mensagem)
    else:
        resultado = False
        mensagem = f"Lote inválido"
        print(mensagem)
        
    return resultado, mensagem



def excluir_lote(id, idusuario, motivo="Exclusão de lote"):
    resultado = False
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Excluir o lote 
        builder = Lote.get_SQLBuilder()
        comandoSQL, valoresFiltro = builder.delete_sql_and_values(Lote(id, None, None, None, None, None, None))
        cursor.execute(comandoSQL, valoresFiltro)
        registrosAfetados = cursor.rowcount

        conexao.commit()
        cursor.close()
        conexao.close()

        if registrosAfetados > 0:
            resultado = True
            mensagem = f"Lote {id} excluído com sucesso"
        else:
            mensagem = f"Lote {id} não encontrado"
    except Exception as e:
        resultado = False
        mensagem = f"Erro ao excluir o lote {id} ({e})"
        print(mensagem)

    return resultado, mensagem

