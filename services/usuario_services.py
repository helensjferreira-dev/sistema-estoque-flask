from conn import conectar
from models.usuarios import Usuario

def listar_todos_usuarios(): 

    builder = Usuario.get_SQLBuilder()
    comandoSQL = builder.build_select()

    resultado=[]
    try:
        conexao=conectar()
        cursor=conexao.cursor() 
        cursor.execute(comandoSQL)
        dados=cursor.fetchall()
        registrosAfetados = cursor.rowcount

        if dados:
            resultado=[Usuario.from_db(item).to_dict() for item in dados]
        else:
            resultado=[]

        cursor.close()
        conexao.close()
        mensagem = f"Foram encontrados {registrosAfetados} registros"

    except Exception as e:
        print(f'Erro ao localizar os usuários {e}')
        print(f"{mensagem} ({e})")
    return resultado, mensagem

def buscar_usuario_por_id(id):

    builder = Usuario.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.select_sql_and_values({"id": id})


    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(comandoSQL, valoresFiltro)
        dados = cursor.fetchone()
        registrosAfetados = cursor.rowcount

        if dados:
            resultado = Usuario.from_db(dados).to_dict()
        else:
            resultado = None

        cursor.close()
        conexao.close()
        mensagem = f"Foram encontrados {registrosAfetados} registros"
        return resultado, mensagem
    except Exception as e:
        print(f"Erro ao localizar o usuário {id}# {e}")
        print(f"{mensagem} ({e})")
        return None, mensagem



def novo_usuario(usuario):
    resultado = False
    if isinstance(usuario, Usuario):
 
        builder = Usuario.get_SQLBuilder()
        comandoSQL, valoresFiltro = builder.insert_sql_and_values(usuario)

        try:    
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute(comandoSQL, valoresFiltro)
            registrosAfetados = cursor.rowcount
            conexao.commit()
            cursor.close()
            conexao.close()

            resultado = True
            mensagem = f"Foram incluidos {registrosAfetados} registros"
        except Exception as e:
            resultado = False
            mensagem = f"Erro ao incluir um nov usuário"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = f"Usuário inválido"
        print(f"{mensagem}")
        
    return resultado, mensagem

def alterar_usuario(usuario):
    resultado = False
    if isinstance(usuario, Usuario):

        builder = Usuario.get_SQLBuilder()
        comandoSQL, valoresFiltro = builder.update_sql_and_values(usuario)

        try:    
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
            mensagem = f"Erro na atualização do usuário"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = f"Usuário inválido"
        print(f"{mensagem}")
        
    return resultado, mensagem


def excluir_usuario(id): 
    builder = Usuario.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.delete_sql_and_values(Usuario(id, None, None, None))

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
        mensagem = f"Erro ao excluir o usuário {id}#"
        print(f"{mensagem}")
        
    return resultado, mensagem

    
# login de acesso (busca pelo email mas confere na rota)
def usuario_login(email):

    try:    
        conexao = conectar()
        cursor = conexao.cursor()

        builder = Usuario.get_SQLBuilder()
        comandoSQL, valoresFiltro = builder.select_sql_and_values({"email": email})

        cursor.execute(comandoSQL, valoresFiltro)
        dados = cursor.fetchone()
        
        cursor.close()
        conexao.close()


        if dados:
            return Usuario(dados[0], dados[1], dados[2], dados[3])
        else:
            return None

    except Exception as e:
        print(f"Erro ao localizar o usuário {e}")
        return None