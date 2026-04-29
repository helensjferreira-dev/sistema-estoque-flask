from util.sqlbuilder import *
from datetime import datetime

from services.fornecedor_services import buscar_fornecedor_por_id

class Lote:

    __tabela_banco__ = "LOTE"

    __campos_tabela__ = {
        "id": "IDLOTE",
        "idproduto": "IDPRODUTO",
        "idfornecedor": "IDFORNECEDOR",
        "data_cadastro": "DATA_CADASTRO",
        "data_validade": "DATA_VALIDADE",
        "numero": "NUMERO",
        "quantidade": "QUANTIDADE"
    }

    __campos_chave__ = ["id"]

    def __init__(self, id, idproduto, idfornecedor, data_cadastro, data_validade, numero, quantidade):
        self.id = id
        self.idproduto = idproduto
        self.idfornecedor = idfornecedor
        self.data_cadastro = data_cadastro
        self.data_validade = data_validade
        self.numero = numero
        self.quantidade = quantidade

    @staticmethod
    def buscar_por_numero(numero):
        from conn import conectar  # ajuste conforme seu helper de conexão
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT idlote, idproduto, idfornecedor, data_cadastro, data_validade, numero, quantidade
            FROM LOTE
            WHERE numero = %s
            LIMIT 1
        """, (numero,))
        row = cur.fetchone()
        cur.close()

        if not row:
            return None

        # Se o cursor retorna dict, ótimo. Se retorna tupla, mapeie manualmente:
        if isinstance(row, dict):
            return row
        return {
            "idlote": row[0],
            "idproduto": row[1],
            "idfornecedor": row[2],
            "data_cadastro": row[3],
            "data_validade": row[4],
            "numero": row[5],
            "quantidade": row[6],
        }

    @classmethod
    def from_db(cls, row):
        if isinstance(row, dict):
            return cls(
                row["IDLOTE"],
                row["IDPRODUTO"],
                row["IDFORNECEDOR"],
                row["DATA_CADASTRO"],
                row["DATA_VALIDADE"],
                row["NUMERO"],
                row["QUANTIDADE"]
            )
        else:
            return cls(
                row[0], row[1], row[2],
                row[3], row[4], row[5], row[6]
            )

    def to_dict(self):
        from services.produto_services import buscar_produto_por_id
        # Formatação das datas
        data_cadastro_formatada = datetime.strftime(self.data_cadastro, "%Y-%m-%d")
        data_validade_formatada = datetime.strftime(self.data_validade, "%Y-%m-%d")

        # Buscar produto completo
        produto, _ = buscar_produto_por_id(self.idproduto)
        if not produto:
            produto = {"nome": "não encontrado"}

        # Buscar fornecedor completo
        fornecedor, _ = buscar_fornecedor_por_id(self.idfornecedor)
        if not fornecedor:
            fornecedor = {"nome": "não encontrado"}

        return {
            "id": self.id,
            "idproduto": self.idproduto,
            "produto": produto,
            "idfornecedor": self.idfornecedor,
            "fornecedor": fornecedor,
            "data_cadastro": data_cadastro_formatada,
            "data_validade": data_validade_formatada,
            "numero": self.numero,
            "quantidade": self.quantidade
        }

    # <<< AQUI ESTÁ CORRIGIDO — FORA DO to_dict() >>>
    def to_insert_db(self):
        return (
            self.idproduto,
            self.idfornecedor,
            self.data_cadastro,
            self.data_validade,
            self.numero,
            self.quantidade
        )

    def to_update_db(self):
        return (
            self.idproduto,
            self.idfornecedor,
            self.data_cadastro,
            self.data_validade,
            self.numero,
            self.quantidade,
            self.id
        )

    @staticmethod
    def get_SQLBuilder():
        return SQLBuilder(Lote.__tabela_banco__, Lote.__campos_tabela__, Lote.__campos_chave__)
