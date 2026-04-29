from conn import conectar
from models.fornecedores import Fornecedor

def listar_todos_fornecedores():
        #montando o comando SQL 
    builder = Fornecedor.get_SQLBuilder()
    comandoSQL = builder.build_select()

    resultado=[]
    try:
        conexao=conectar()
        cursor=conexao.cursor() 
        cursor.execute(comandoSQL)
        dados=cursor.fetchall()
        registrosAfetados = cursor.rowcount

        if dados:
            resultado=[Fornecedor.from_db(item).to_dict() for item in dados]
        else:
            resultado=[]

        cursor.close()
        conexao.close()
        mensagem = f"Foram encontrados {registrosAfetados} registros"

    except Exception as e:
        mensagem = f"Erro ao localizar os fornecedores"
        print(f"{mensagem} ({e})")
    
    return resultado, mensagem

def buscar_fornecedor_por_id(id):
    builder = Fornecedor.get_SQLBuilder()
    sql, valores = builder.select_sql_and_values({"id": id})

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(sql, valores)
        dado = cur.fetchone()

        if dado:
            fornecedor = Fornecedor.from_db(dado).to_dict()
            return fornecedor, "OK"
        else:
            return None, "Fornecedor não encontrado"

    except Exception as e:
        print("Erro:", e)
        return None, "Erro"


    
def novo_fornecedor(fornecedor):
    resultado = False
    if isinstance(fornecedor, Fornecedor):
        try:

            builder = Fornecedor.get_SQLBuilder()
            comandoSQL, valoresFiltro = builder.insert_sql_and_values(fornecedor)

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
            mensagem = f"Erro ao incluir um novo fornecedor"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = f"Fornecedor inválido"
        print(f"{mensagem}")
        
    return resultado, mensagem

def atualizar_fornecedor(fornecedor):
    resultado = False
    if isinstance(fornecedor, Fornecedor):
        try:
            builder = Fornecedor.get_SQLBuilder()
            comandoSQL, valoresFiltro = builder.update_sql_and_values(fornecedor)

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
            mensagem = f"Erro na atualização do fornecedor"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = f"Fornecedor inválido"
        print(f"{mensagem}")
        
    return resultado, mensagem

def excluir_fornecedor(id): 
    builder = Fornecedor.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.delete_sql_and_values(Fornecedor(id, None, None, None))

    resultado = False
    try:    
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL, valoresFiltro)
        registrosAfetados = cursor.rowcount
        conexao.commit()
        cursor.close()
        conexao.close()

        resultado = True
        mensagem = f"Foram excluidos {registrosAfetados} registros"
    except Exception as e:
        resultado = False
        mensagem = f"Erro ao excluir o fornecedor {id}#"
        print(f"{mensagem} ({e})")
        
    return resultado, mensagem
