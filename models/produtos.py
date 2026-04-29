from util.sqlbuilder import *

class Produto:
    __tabela_banco__ = "PRODUTO"

    __campos_tabela__ = {
        "id": "IDPRODUTO",
        "idcategoria": "IDCATEGORIA",
        "nome": "NOME",
        "descricao": "DESCRICAO",
        "controle_validade": "CONTROLE_VALIDADE",
        "estoque_minimo": "ESTOQUE_MINIMO"
    }

    __campos_chave__ = ["id"]

    def __init__(self, id, idcategoria, nome, descricao, controle_validade, estoque_minimo):
        self.id = id
        self.idcategoria = idcategoria
        self.nome = nome
        self.descricao = descricao
        self.controle_validade = controle_validade
        self.estoque_minimo = estoque_minimo

    @classmethod
    def from_db(cls, row):
        if isinstance(row, dict):
            return cls(
                row["IDPRODUTO"], row["IDCATEGORIA"], row["NOME"],
                row.get("DESCRICAO"), row["CONTROLE_VALIDADE"], row.get("ESTOQUE_MINIMO")
            )
        return cls(row[0], row[1], row[2], row[3], row[4], row[5])

    def to_dict(self):
        return {
            "id": self.id,
            "idcategoria": self.idcategoria,
            "nome": self.nome,
            "descricao": self.descricao,
            "controle_validade": self.controle_validade,
            "estoque_minimo": self.estoque_minimo
        }

    def to_insert_db(self):
        return (self.idcategoria, self.nome, self.descricao, self.controle_validade, self.estoque_minimo)

    def to_update_db(self):
        return (self.idcategoria, self.nome, self.descricao, self.controle_validade, self.estoque_minimo, self.id)

    def get_SQLBuilder():
        return SQLBuilder(Produto.__tabela_banco__, Produto.__campos_tabela__, Produto.__campos_chave__)
 