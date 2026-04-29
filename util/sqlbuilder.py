class SQLBuilder:
    def __init__(self, tabela, depara, campos_chave):
        """
        tabela: nome da tabela no banco
        depara: dicionário {atributo_da_classe: coluna_no_banco}
        campos_chave: lista ou tupla com os nomes dos atributos-chave
        """
        self.tabela = tabela
        self.depara = depara
        self.campos_chave = list(campos_chave)

    # ------------------------------------------------------------
    # Métodos básicos de construção SQL
    # ------------------------------------------------------------

    def build_insert(self, usarChave = False):
        # verifica se é necessario usar a chave, quando tem auto_increment não precisa
        if usarChave:
            colunas = [self.depara[c] for c in self.depara]
        else:
            colunas = [self.depara[c] for c in self.depara if c not in self.campos_chave]

        # montando a parte os campos do join
        campos = ", ".join(colunas)

        # criando um paramentro para cada campo do join
        valores = ", ".join(["%s"] * len(colunas))

        # concatenando o comando com a tabela, os campos, e os indicadores de paramentros
        sql = f"INSERT INTO {self.tabela} ({campos}) VALUES ({valores})"

        return sql

    def build_update(self):
        # criando a parte do set, onde tem a combinação de campo operador de atribuição (=) e o paramentro para ser preenchido
        set_clause = ", ".join([
            f"{self.depara[c]} = %s" for c in self.depara if c not in self.campos_chave
        ])

        # criando a parte do where, onde tem a combinação de campo operador (=) e o paramentro para ser preenchido normalmente usando a chave primaria da tabela
        where_clause = " AND ".join([
            f"{self.depara[c]} = %s" for c in self.campos_chave
        ])

        # concatenando o comando com a tabela, os campos e o where
        sql = f"UPDATE {self.tabela} SET {set_clause} WHERE {where_clause}"

        return sql

    def build_select(self, filtros=None):
        """
        filtros: dicionário opcional {atributo: valor}
        """
        # criando a parte do select onde vai a lista de campo separado por ,
        colunas = ", ".join([self.depara[c] for c in self.depara])
        # montando o select        
        sql = f"SELECT {colunas} FROM {self.tabela}"

        # se foi informado um filtro é construido com campo operador e parametro
        if filtros:
            where = self._build_where_clause(filtros)
            sql += f" WHERE {where}"

        return sql

    def build_delete(self):
        # criando a parte do where para restringir o comando delete
        where_clause = " AND ".join([
            f"{self.depara[c]} = %s" for c in self.campos_chave
        ])

        #montando o comando delete
        sql = f"DELETE FROM {self.tabela} WHERE {where_clause}"

        return sql

    # ------------------------------------------------------------
    # Auxiliares
    # ------------------------------------------------------------

    def _build_where_clause(self, filtros):
        """
        Monta cláusula WHERE dinâmica.
        filtros = {"nome": "Camiseta", "ativo": True}
        → "NOME = %s AND ATIVO = %s"
        """
        return " AND ".join([f"{self.depara[c]} = %s" for c in filtros])

    # ------------------------------------------------------------
    # Geração de SQL + valores
    # ------------------------------------------------------------

    def insert_sql_and_values(self, obj, usarChave = False):
        # chama a função que monta o comando SQL
        sql = self.build_insert(usarChave)

        # cria uma lista na ordem necessaria com o valores  da classe que vão substituir os paramentros dos comandos
        if usarChave:
            valores = [getattr(obj, c) for c in self.depara]
        else:
            valores = [getattr(obj, c) for c in self.depara if c not in self.campos_chave]

        return sql, valores

    def update_sql_and_values(self, obj):
        # chama a função que monta o comando SQL
        sql = self.build_update()

        # cria uma lista na ordem necessaria com o valores  da classe que vão substituir os paramentros dos comandos
        valores_set = [getattr(obj, c) for c in self.depara if c not in self.campos_chave]
        valores_where = [getattr(obj, c) for c in self.campos_chave]

        return sql, valores_set + valores_where

    def delete_sql_and_values(self, obj):
        # chama a função que monta o comando SQL
        sql = self.build_delete()

        # cria uma lista na ordem necessaria com o valores  da classe que vão substituir os paramentros dos comandos
        valores = [getattr(obj, c) for c in self.campos_chave]
        return sql, valores

    def select_sql_and_values(self, filtros=None):
        # chama a função que monta o comando SQL
        sql = self.build_select(filtros)

        # cria uma lista na ordem necessaria com o valores  da classe que vão substituir os paramentros dos comandos
        valores = [filtros[c] for c in filtros] if filtros else []
        return sql, valores
