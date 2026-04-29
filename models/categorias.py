from util.sqlbuilder import *

class Categoria:
    __tabela_banco__ = "CATEGORIA"

    __campos_tabela__ = {
        "id": "IDCATEGORIA",
        "nome": "NOME"
    }

    __campos_chave__ = ["id"]

    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @classmethod
    def from_db(cls, row):
        if isinstance(row, dict):
            return cls(row["IDCATEGORIA"], row["NOME"])
        return cls(row[0], row[1])

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}

    def to_insert_db(self):
        return (self.nome,)

    def to_update_db(self):
        return (self.nome, self.id)

    def get_SQLBuilder():
        return SQLBuilder(Categoria.__tabela_banco__, Categoria.__campos_tabela__, Categoria.__campos_chave__)
