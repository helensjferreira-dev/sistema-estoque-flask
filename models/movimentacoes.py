# models/movimentacoes.py
from util.sqlbuilder import SQLBuilder
from datetime import datetime

class Movimentacao:
    __tabela_banco__ = "MOVIMENTACAO"

    __campos_tabela__ = {
        "id": "IDMOVIMENTACAO",
        "idlote": "IDLOTE",
        "idusuario": "IDUSUARIO",
        "data_movimentacao": "DATA_MOVIMENTOCAO",
        "tipo": "TIPO",
        "quantidade": "QUANTIDADE",
        "valor_unitario": "VALOR_UNITARIO",
        "motivo": "MOTIVO",
    }

    __campos_chave__ = ["id"]

    def __init__(self, id, idlote, idusuario, data_movimentacao, tipo, quantidade, valor_unitario, motivo):
        self.id = id
        self.idlote = idlote
        self.idusuario = idusuario

        # aceita string "YYYY-MM-DD" ou datetime ou None
        if isinstance(data_movimentacao, str):
            try:
                self.data_movimentacao = datetime.strptime(data_movimentacao, "%Y-%m-%d")
            except Exception:
                self.data_movimentacao = None
        else:
            self.data_movimentacao = data_movimentacao

        self.tipo = tipo
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.motivo = motivo

    @classmethod
    def from_db(cls, row):
        # row pode ser dict (RealDictCursor) ou tupla (cursor padrão)
        if isinstance(row, dict):
            return cls(
                row.get("IDMOVIMENTACAO"),
                row.get("IDLOTE"),
                row.get("IDUSUARIO"),
                row.get("DATA_MOVIMENTOCAO"),
                row.get("TIPO"),
                row.get("QUANTIDADE"),
                row.get("VALOR_UNITARIO"),
                row.get("MOTIVO"),
            )
        else:
            # tupla — atenção à ordem se usar SELECT com JOINs diferentes
            return cls(
                row[0],  # IDMOVIMENTACAO
                row[1],  # IDLOTE
                row[2],  # IDUSUARIO
                row[3],  # DATA_MOVIMENTOCAO
                row[4],  # TIPO
                row[5],  # QUANTIDADE
                row[6],  # VALOR_UNITARIO
                row[7],  # MOTIVO
            )

    def to_dict(self):
        data_fmt = None
        if isinstance(self.data_movimentacao, datetime):
            data_fmt = self.data_movimentacao.strftime("%Y-%m-%d")
        elif isinstance(self.data_movimentacao, str):
            data_fmt = self.data_movimentacao

        return {
            "idmovimentacao": self.id,
            "idlote": self.idlote,
            "idusuario": self.idusuario,
            "data_movimentacao": data_fmt,
            "tipo": self.tipo,
            "quantidade": self.quantidade,
            "valor_unitario": float(self.valor_unitario) if self.valor_unitario is not None else None,
            "motivo": self.motivo,
        }

    def to_insert_db(self):
        return (
            self.idlote,
            self.idusuario,
            self.data_movimentacao,
            self.tipo,
            self.quantidade,
            self.valor_unitario,
            self.motivo,
        )

    def to_update_db(self):
        return (
            self.idlote,
            self.idusuario,
            self.data_movimentacao,
            self.tipo,
            self.quantidade,
            self.valor_unitario,
            self.motivo,
            self.id,
        )

    @staticmethod
    def get_SQLBuilder():
        return SQLBuilder(Movimentacao.__tabela_banco__, Movimentacao.__campos_tabela__, Movimentacao.__campos_chave__)
