#Importando as bibliotecas

from flask import Flask, jsonify, request, render_template, Blueprint, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session
import traceback


from routes.categoria_routes import categoria_routes 
from routes.fornecedor_routes import fornecedor_routes
from routes.produto_routes import produto_routes
from routes.lote_routes import lote_routes
from routes.movimentacao_routes import movimentacao_routes
from routes.usuario_routes import usuario_routes
from routes.relatorio_routes import relatorio_routes

from util.carga import *

#Importando a conexão
from conn import conectar

#Construindo a aplicação web com o Flask
app = Flask(__name__)
CORS(app) #ignorar os erros de segurança


@app.route('/', endpoint='inicial')
def inicial():
    return render_template("index.html")


@app.route('/status')
def conexao():
    try:
        conexao = conectar()
        conexao.close()
        mensagem="Banco de dados conectado"
    except:
        mensagem="Atenção, banco de dados desconectado"

    return jsonify({"mensagem":"Backend funcionando", "Banco":mensagem})

@app.errorhandler(404)
def mensagem_rota_invalida(error): 
    return render_template('404.html'), 404 

@app.errorhandler(500)
def mensagem_erro_interno(error):
    mensagem=str(error)
    tb_mensagem=traceback.format_exc()
    return render_template('500.html', erro=mensagem, tb=tb_mensagem), 500 


#Registros das rotas

app.register_blueprint(categoria_routes)
app.register_blueprint(fornecedor_routes)
app.register_blueprint(lote_routes)
app.register_blueprint(produto_routes)
app.register_blueprint(movimentacao_routes)
app.register_blueprint(usuario_routes)
app.register_blueprint(relatorio_routes)

#Escondendo as senhas
app.secret_key = 'sua_chave_secreta_segura' 
app.config['SESSION_TYPE'] = 'filesystem'    # Armazena sessão no sistema de arquivos
Session(app)




# quando o banco de dados for reiniciado, esse método faz uma carga para teste
@app.route('/carga_inicial', methods=["GET"])
def carga_inicial():
    carga_de_dados()
    return jsonify({"mensagem":"Dados incluidos"})



if __name__ == "__main__": 
    # Habilitando o log do console das solicitações
    app.run(debug=True)