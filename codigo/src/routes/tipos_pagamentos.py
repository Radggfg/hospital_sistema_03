# Rotas do módulo financeiro para controle de pagamentos e tipos de pagamento
from flask import Blueprint, request
from src import banco
from src.db import pagamentos, despesas_hospitalares
from sqlalchemy import select
from datetime import datetime
from sqlalchemy import select
from flask import jsonify

# Definição do blueprint com prefixo de rota '/financeiro'
tipo_pagamento = Blueprint("tipo_pagamento",__name__,url_prefix = "/tipo_pagamento")
pagamento = Blueprint("pagamento",__name__,url_prefix = "/pagamento")
despesa_hospitalar = Blueprint("despesa_hospitalar",__name__,url_prefix = "/despesa_hospitalar")

# Cadastrar novo tipo de pagamento
@tipo_pagamento.route("/cadastrar_tipo_pagamento", methods=["POST"])
def cadastrar_tipo_pagamento():
    nome_tipo_pagamento = request.form.get("nome_tipo_pagamento")

    if not nome_tipo_pagamento:
        return{"sucess":False, "message": "nome_tipo_pagamento é obrigatório!"}, 400

    novo_tipo_pagamento = pagamentos.Tipo_Pagamento(nome_tipo_pagamento = nome_tipo_pagamento)
    try:
        banco.session.add(novo_tipo_pagamento)
        banco.session.commit()
        return{"sucess":True, "message": "Tipo_pagamento cadastrado!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao inserir no banco de dados!"}, 400



# Listar todos os tipos de pagamento
@tipo_pagamento.route("/listar_tipo_pagamento", methods=["GET"])
def listar_tipo_pagamento():
    tipos_pagamentos_query = select(
        pagamentos.Tipo_Pagamento.id_tipo_pagamento,
        pagamentos.Tipo_Pagamento.nome_tipo_pagamento
    )
    todos_tipos_pagamentos = banco.session.execute(tipos_pagamentos_query).all()
    lista = []
    for pag in todos_tipos_pagamentos:
        lista.append({
            "id_tipo_pagamento":pag.id_tipo_pagamento,
            "nome_tipo_pagamento":pag.nome_tipo_pagamento
        })
    return{"sucess":True, "todos_tipos_pagamentos":lista}


# Rota para buscar tipo_pagamento por ID do tipo_pagamento
@tipo_pagamento.route("/buscar_tipo_pagamento", methods=["GET"])
def buscar_tipo_pagamento():
    id_tipo_pagamento = request.form.get("id_tipo_pagamento")
    if not id_tipo_pagamento:
        return{"sucess":False, "message": "O id_tipo_pagamento é obrigatório!"}, 400
    try:
        tipos_pagamentos_query = banco.session.query(pagamentos.Tipo_Pagamento).where(pagamentos.Tipo_Pagamento.id_tipo_pagamento==id_tipo_pagamento).first()
        if not tipos_pagamentos_query:
            return{"sucess":False, "message": "Tipo de pagamento não encontrado!"}, 400
        resultado = {
            "id_tipo_pagamento":tipos_pagamentos_query.id_tipo_pagamento,
            "nome_tipo_pagamento":tipos_pagamentos_query.nome_tipo_pagamento,
        }
        return {"sucess": True, "tipos_pagamentos_query": resultado}
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "O id_tipo_pagamento não foi encontrado!"}, 400





# Deletar um tipo de pagamento
@tipo_pagamento.route("/deletar_tipo_pagamento", methods=["DELETE"])
def deletar_tipo_pagamento():
    id_tipo_pagamento = request.form.get("id_tipo_pagamento")
    query_pagamento = banco.session.query(pagamentos.Tipo_Pagamento).where(pagamentos.Tipo_Pagamento.id_tipo_pagamento==id_tipo_pagamento).first()
    try:
        banco.session.delete(query_pagamento)
        banco.session.commit()
        return{"sucess":True, "message": "Tipo de pagamento deletado com sucesso!"}, 201
    except Exception as err:
        return{"sucess":False, "message": "Falha ao deletar o tipo de pagamento!"}, 400






# Listar todos os pagamentos
@pagamento.route("/listar_todo_pagamento", methods=["GET"])
def listar_todos_pagamentos():
    try:
        tipos_pagamentos_query = select(
            pagamentos.Pagamento.id_pagamento,
            pagamentos.Pagamento.status_pagamento,
            pagamentos.Pagamento.data_pagamento,
            pagamentos.Pagamento.num_parcelas,
            pagamentos.Pagamento.valor_pago,
            pagamentos.Pagamento.fluxo_pagamento,
            pagamentos.Pagamento.tipo_pagamento,
        )

        resultados = banco.session.execute(tipos_pagamentos_query).all()

        lista = []
        for pag in resultados:
            lista.append({
                "id_pagamento": pag.id_pagamento,
                "status_pagamento": pag.status_pagamento,
                "data_pagamento": pag.data_pagamento.strftime("%d/%m/%Y %H:%M:%S") if pag.data_pagamento else None,
                "num_parcelas": pag.num_parcelas,
                "valor_pago": pag.valor_pago,
                "fluxo_pagamento": pag.fluxo_pagamento,
                "tipo_pagamento": pag.tipo_pagamento,
            })

        return {"success": True, "todos_pagamentos": lista}
    
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"success": False, "message": "Erro ao listar os pagamentos!"}, 400



# Consultar pagamento por ID
@pagamento.route("/consultar_pagamento", methods=["GET"])
def consultar_pagamentos():
    id_pagamento = request.form.get("id_pagamento")
    if not id_pagamento:
        return {"success": False, "message": "O id_pagamento é obrigatório!"}, 400
    try:
        query_pagamento = banco.session.query(pagamentos.Pagamento).where(
            pagamentos.Pagamento.id_pagamento == id_pagamento
        ).first()
        if not query_pagamento:
            return {"success": False, "message": "O id_pagamento não foi cadastrado"}, 400

        resultado = {
            "id_pagamento": query_pagamento.id_pagamento,
            "status_pagamento": query_pagamento.status_pagamento,
            "data_pagamento": query_pagamento.data_pagamento.strftime("%d/%m/%Y %H:%M:%S") if query_pagamento.data_pagamento else None,
            "num_parcelas": query_pagamento.num_parcelas,
            "valor_pago": query_pagamento.valor_pago,
            "fluxo_pagamento": query_pagamento.fluxo_pagamento,
            "tipo_pagamento": query_pagamento.tipo_pagamento,
        }
        return {
            "success": True,
            "message": "O id_pagamento foi encontrado!",
            "pagamento": resultado
        }
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"success": False, "message": "Erro ao obter o pagamento!"}, 400




# Criar um novo pagamento
@pagamento.route("/criar_pagamento",methods = ["POST"])
def criar_pagamento():
    status_pagamento = request.form.get("status_pagamento")
    data_pagamento = request.form.get("data_pagamento")
    num_parcelas = request.form.get("num_parcelas")
    valor_pago = request.form.get("valor_pago")
    fluxo_pagamento = request.form.get("fluxo_pagamento")

    data_pagamento = datetime.strptime(data_pagamento, "%d/%m/%Y %H:%M:%S")

    if not status_pagamento or not data_pagamento or not num_parcelas or not valor_pago or not fluxo_pagamento or not data_pagamento:
        return{"sucess":False, "message": "status_pagamento, data_pagamento, num_parcelas, valor_pago, fluxo_pagamento e data_pagamento são obrigatórios!"}, 400

    novo_pagamento = pagamentos.Pagamento(status_pagamento = status_pagamento,
                                        data_pagamento = data_pagamento,
                                        num_parcelas = num_parcelas,
                                        valor_pago = valor_pago,
                                        fluxo_pagamento = fluxo_pagamento)
    try:
        banco.session.add(novo_pagamento)
        banco.session.commit()
        return{"sucess":True, "message": "Pagamento cadastrado com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao cadastrar o pagamento!"}, 400


