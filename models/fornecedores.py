from util.sqlbuilder import *
from datetime import datetime

class Fornecedor:
        # definição da tabela que vai salvar os dados 
    __tabela_banco__ = "FORNECEDOR"

    # relacionando nome da classe com o nome do campo na tabela
    __campos_tabela__ = {
        "id":"IDFORNECEDOR"
        ,"nome":"NOME"
        ,"telefone":"TELEFONE"
        ,"email":"EMAIL"
    }

    # definição dos campos chave da tabela
    __campos_chave__ = ["id"]

    def __init__(self, id, nome, telefone, email):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
 
    @classmethod
    def from_db(cls, row):
        if isinstance(row, dict):
            fornecedor= cls(row["IDFORNECEDOR"], row["NOME"], row["TELEFONE"], row["EMAIL"])
        else:
            return cls(row[0], row[1], row[2], row[3])
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email                    
        }
    def to_insert_db(self):
        """
        Esse metodo retorna um tupla com os valores a serem usado para insert do banco de dados, 
        deve retornar os campos na ordem do insert e não tem o id, porque o id é gerado pelo banco de dados
        """
        return (self.nome, self.telefone, self.email)

    def to_update_db(self):
        """
        Esse metodo retorna um tupla com os valores a serem usado para update do banco de dados, 
        deve retornar os campos na ordem do update e o id no final, porque o id é usado no where que vem depois dos valores
        """
        return (self.nome, self.telefone, self.email, self.id)

    def get_SQLBuilder():
        """
        Esse metodo retorna objeto que monta os comandos sql de acordo com o nome da tabela e campos declarados no inicio da classe
        """
        return SQLBuilder(Fornecedor.__tabela_banco__, Fornecedor.__campos_tabela__, Fornecedor.__campos_chave__)    