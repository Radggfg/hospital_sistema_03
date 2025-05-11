from flask import Blueprint, request
from src import banco
from src.db import estoque_hospitalar
from datetime import datetime
from sqlalchemy import select

# Define o blueprint para rotas de estoque hospitalar
estoque = Blueprint("estoque_hospitalar", __name__, url_prefix="/estoque_hospitalar")

# Rota para criar um novo item no estoque
@estoque.route('/criar_estoque', methods=['POST'])
def criar_item_estoque():
    id_produto = request.form.get("id_produto")
    categoria = request.form.get("categoria")
    quantidade = request.form.get("quantidade")
    data_entrada = request.form.get("data_entrada")
    data_atualizacao = request.form.get("data_atualizacao")
    status = request.form.get("status")

    # Validação dos campos obrigatórios
    if not id_produto or not categoria or not quantidade or not data_entrada or not status:
        return {"sucess": False, "message": "id_produto, categoria, quantidade, data_entrada e status são obrigatórios!"}, 400

    # Conversão das datas
    data_entrada = datetime.strptime(data_entrada, "%d/%m/%Y %H:%M")
    data_atualizacao = datetime.strptime(data_atualizacao, "%d/%m/%Y %H:%M")

    # Cria novo objeto do estoque
    novo_item = estoque_hospitalar.Estoque_hospitalar(
        id_produto=id_produto,
        categoria=categoria,
        quantidade=quantidade,
        data_entrada=data_entrada,
        data_atualizacao=data_atualizacao,
        status=status
    )

    # Insere no banco
    try:
        banco.session.add(novo_item)
        banco.session.commit()
        return {"sucess": True, "message": "Item acrescentado com sucesso ao sistema!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao acrescentar o item ao sistema!"}, 400


# Rota para listar todos os itens do estoque
@estoque.route('/listar_estoque', methods=['GET'])
def listar_estoque():
    estoque_query = select(
        estoque_hospitalar.Estoque_hospitalar.id_produto,
        estoque_hospitalar.Estoque_hospitalar.categoria,
        estoque_hospitalar.Estoque_hospitalar.quantidade,
        estoque_hospitalar.Estoque_hospitalar.data_entrada,
        estoque_hospitalar.Estoque_hospitalar.data_atualizacao,
        estoque_hospitalar.Estoque_hospitalar.status
    )
    todos_estoques = banco.session.execute(estoque_query).all()
    lista = []
    for item in todos_estoques:
        lista.append({
            "id_produto": item.id_produto,
            "categoria": item.categoria,
            "quantidade": item.quantidade,
            "data_entrada": item.data_entrada,
            "data_atualizacao": item.data_atualizacao,
            "status": item.status
        })
    return {"sucess": True, "todos_estoques": lista}


# Rota para buscar item por ID do estoque
@estoque.route('/buscar_estoque', methods=['GET'])
def buscar_item_estoque():
    id_estoque = request.form.get("id_estoque")
    if not id_estoque:
        return {"sucess": False, "message": "id_estoque é obrigatório!"}, 400
    try:
        query_estoque = banco.session.query(estoque_hospitalar.Estoque_hospitalar).filter_by(id_estoque=id_estoque).first()
        if not query_estoque:
            return {"sucess": False, "message": "Item não encontrado."}, 404
        resultado = {
            "id_estoque": query_estoque.id_estoque,
            "id_produto": query_estoque.id_produto,
            "categoria": query_estoque.categoria,
            "quantidade": query_estoque.quantidade,
            "data_entrada": query_estoque.data_entrada,
            "data_atualizacao": query_estoque.data_atualizacao,
            "status": query_estoque.status
        }
        return {"sucess": True, "item_estoque": resultado}
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "O id_estoque não foi encontrado!"}, 400


# Rota para atualizar item do estoque
@estoque.route('/atualizar_estoque', methods=['PUT'])
def atualizar_item_estoque():
    id_estoque = request.form.get("id_estoque")
    if not id_estoque:
        return {"sucess": False, "message": "id_estoque é obrigatório!"}, 400

    nova_quantidade = request.form.get("quantidade")
    nova_data_entrada = request.form.get("data_entrada")
    nova_data_atualizacao = request.form.get("data_atualizacao")
    novo_status = request.form.get("status")

    try:
        query_estoque = banco.session.query(estoque_hospitalar.Estoque_hospitalar).filter_by(id_estoque=id_estoque).first()
        if nova_quantidade:
            query_estoque.quantidade = nova_quantidade
        if nova_data_entrada:
            query_estoque.data_entrada = datetime.strptime(nova_data_entrada, "%d/%m/%Y %H:%M")
        if nova_data_atualizacao:
            query_estoque.data_atualizacao = datetime.strptime(nova_data_atualizacao, "%d/%m/%Y %H:%M")
        if novo_status:
            query_estoque.status = novo_status
        banco.session.commit()
        return {"sucess": True, "message": "Dados do estoque atualizados com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao atualizar os dados do estoque!"}, 400


# Rota para deletar item do estoque
@estoque.route('/deletar_estoque', methods=['DELETE'])
def deletar_item_estoque():
    id_estoque = request.form.get("id_estoque")
    query_estoque = banco.session.query(estoque_hospitalar.Estoque_hospitalar).filter_by(id_estoque=id_estoque).first()
    try:
        banco.session.delete(query_estoque)
        banco.session.commit()
        return {"sucess": True, "message": "Item deletado com sucesso do estoque!"}, 201
    except Exception as err:
        return {"sucess": False, "message": "Falha ao deletar o item do estoque!"}, 400
