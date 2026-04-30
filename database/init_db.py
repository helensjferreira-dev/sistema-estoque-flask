from conn import conectar

def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    with open("database/schema.sql", "r", encoding="utf-8") as arquivo:
        comandos_sql = arquivo.read()

    for comando in comandos_sql.split(";"):
        comando = comando.strip()
        if comando:
            cursor.execute(comando)

    conexao.commit()
    cursor.close()
    conexao.close()

    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    inicializar_banco()