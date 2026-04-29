from werkzeug.security import generate_password_hash

from models.usuarios import *
from models.categorias import *
from models.fornecedores import *
from models.produtos import *
from models.lotes import *
from models.movimentacoes import *

from services.usuario_services import *
from services.categoria_services import *
from services.fornecedor_services import *
from services.produto_services import *
from services.lote_services import *
from services.movimentacao_services import *

def carga_de_dados():

    # criando usuario
    usuario = Usuario(None, 'admin', 'admin@email.com', generate_password_hash('123'))
    novo_usuario(usuario)    

    # criando categorias
    categorias = [Categoria(None, 'hidratante'), Categoria(None, 'Instrumentos')]
    for categoria in categorias:
        nova_categoria(categoria)

    # criando fornecedores
    fornecedores = [Fornecedor(None, 'Loja 1', "11223344", "loja1@email.com"), 
                    Fornecedor(None, 'Loja 2', "8899775522", "loja2@email.com")
                ]
    for fornecedor in fornecedores:
        novo_fornecedor(fornecedor)

    # criando produtos
    produtos = [
                Produto(None, 1, "Creme hidratente", "Creme hidratente para as mãos", "S", 5),
                Produto(None, 2, "Alicate cuticula", "Alicate cuticula", "N", 2),
                Produto(None, 2, "Cortador de unha", "Cortador de unha", "N", 0)
            ]
    for produto in produtos:
        novo_produto(produto)

    # criando lotes para movimentacao
    lotes = [
            Lote(None, 1, 1, "2025-10-01", "2025-10-31", "f14d2", 0),
            Lote(None, 1, 1, "2025-10-01", "2025-10-29", "g45df", 0),
            Lote(None, 2, 2, "2025-10-01", "2027-01-01", "", 0),
            Lote(None, 3, 2, "2025-10-01", "2027-01-01", "", 0)
        ]
    for lote in lotes:
        novo_lote(lote)
        

    # criando lotes para movimentacao
    movimentacoes = [
            Movimentacao(None, 1, 1, "2025-10-25", "ENTRADA", 2, 2.2, "Aquisição de produtos"),
            Movimentacao(None, 2, 1, "2025-10-25", "ENTRADA", 2, 2.1, "Aquisição de produtos"),
            Movimentacao(None, 2, 1, "2025-10-25", "SAIDA", 2, 5, "Uso no atendimento ao cliente"),
            Movimentacao(None, 3, 1, "2025-10-25", "ENTRADA", 1, 7.99, "Aquisição de instrumentos"),
            Movimentacao(None, 4, 1, "2025-10-25", "ENTRADA", 1, 3.65, "Aquisição de instrumentos"),
        ]
    for movimentacao in movimentacoes:
        nova_movimentacao(movimentacao)
