from util.sqlbuilder import *
from datetime import datetime


class Usuario:
    # definição da tabela que vai salvar os dados 
    __tabela_banco__ = "USUARIO"

        # relacionando nome da classe com o nome do campo na tabela
    __campos_tabela__ = {
        "id":"IDUSUARIO"
        ,"nome":"NOME"
        ,"email":"EMAIL"
        ,"senha":"SENHA"
    }
    # definição dos campos chave da tabela
    __campos_chave__ = ["id"]

    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha        

    @classmethod
    def from_db(cls, row):
        """
        Esse metodo pega a linha do curso e converte um objeto
        cls é como se fosse o self
        row é a linha do fechall ou o resultado do fechone

        Podendo ainda usar um dic ou tupla
        exemplo (dic): {"id":1, "descricao":"ifood", "categoria":"alimentacao", "valor":10, "data":"25/09/2025"}
        exemplo (tupla): (1, "ifood", "alimentacao", 10, '25/09/2025')
        """              
        if isinstance(row, dict):
            usuario= cls(row["IDUSUARIO"], row["NOME"], row["EMAIL"], row["SENHA"])
        else:
            return cls(row[0], row[1], row[2], row[3])
        return usuario
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,           
        }
    
    def to_insert_db(self):
        """
        Esse metodo retorna um tupla com os valores a serem usado para insert do banco de dados, 
        deve retornar os campos na ordem do insert e não tem o id, porque o id é gerado pelo banco de dados
        """
        return (self.nome, self.email, self.senha)

    def to_update_db(self):
        """
        Esse metodo retorna um tupla com os valores a serem usado para update do banco de dados, 
        deve retornar os campos na ordem do update e o id no final, porque o id é usado no where que vem depois dos valores
        """
        return (self.nome, self.email, self.senha, self.id)

    def to_dict(self):
        return {"id":self.id
                , "nome": self.nome
                , "email": self.email
                , "senha": self.senha
            }
    
    def get_SQLBuilder():
        """
        Esse metodo retorna objeto que monta os comandos sql de acordo com o nome da tabela e campos declarados no inicio da classe
        """
        return SQLBuilder(Usuario.__tabela_banco__, Usuario.__campos_tabela__, Usuario.__campos_chave__)    