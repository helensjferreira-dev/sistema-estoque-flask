from conn import conectar
from models.categorias import Categoria


def listar_todas_categorias():
    # montando o comando SQL
    builder = Categoria.get_SQLBuilder()
    comandoSQL = builder.build_select()
    resultado = []
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL)
        dados = cursor.fetchall()
        registrosAfetados = cursor.rowcount

        if dados:
            resultado = [Categoria.from_db(item).to_dict() for item in dados]
        else:
            resultado = []

        cursor.close()
        conexao.close()
        mensagem = f"Foram encontrados {registrosAfetados} registros"
    except Exception as e:
        mensagem = "Erro ao localizar as categorias"
        print(f"{mensagem} ({e})")

    return resultado, mensagem


def buscar_categoria_por_id(id):

    builder = Categoria.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.select_sql_and_values({"id": id})
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(comandoSQL, valoresFiltro)
        dados = cursor.fetchone()
        registrosAfetados = cursor.rowcount

        # pegando os dados do banco e convertendo para objeto
        if dados:
            resultado = Categoria.from_db(dados).to_dict()
        else:
            resultado = None

        cursor.close()
        conexao.close()
        mensagem = f"Foram encontrados {registrosAfetados} registros"
        return resultado, mensagem
    except Exception as e:
        mensagem = f"Erro ao localizar a categoria {id}#"
        print(f"{mensagem} ({e})")
        return None, mensagem


def nova_categoria(categoria):
    resultado = False
    if isinstance(categoria, Categoria):

        builder = Categoria.get_SQLBuilder()
        comandoSQL, valoresFiltro = builder.insert_sql_and_values(categoria)
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
            mensagem = "Erro ao incluir uma nova categoria"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = "Categoria inválida"
        print(mensagem)

    return resultado, mensagem


def atualizar_categoria(categoria):
    resultado = False
    if isinstance(categoria, Categoria):

        builder = Categoria.get_SQLBuilder()
        comandoSQL, valoresFiltro = builder.update_sql_and_values(categoria)
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
            mensagem = "Erro na atualização da categoria"
            print(f"{mensagem} ({e})")
    else:
        resultado = False
        mensagem = "Categoria inválida"
        print(mensagem)

    return resultado, mensagem


def excluir_categoria(id):
    builder = Categoria.get_SQLBuilder()
    comandoSQL, valoresFiltro = builder.delete_sql_and_values(Categoria(id, None))
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
        mensagem = f"Erro ao excluir a categoria {id}#"
        print(f"{mensagem} ({e})")

    return resultado, mensagem

def existe_categoria_com_nome(nome, id_ignorar=None):
    """
    Verifica se já existe uma categoria com o mesmo nome.
    Se id_ignorar for informado, ignora esse registro (útil no update).
    """
    try:
        con = conectar()
        cur = con.cursor()
        sql = "SELECT ID FROM CATEGORIA WHERE LOWER(NOME) = LOWER(%s)"
        cur.execute(sql, (nome,))
        row = cur.fetchone()
        cur.close()
        con.close()

        if row:
            #Se for update, ignora se o ID encontrado for o mesmo
            if id_ignorar and str(row[0]) == str(id_ignorar):
                return False
            return True
        return False
    except Exception as e:
        print("ERRO ao verificar categoria existente:", e)
        return False