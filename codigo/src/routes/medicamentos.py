# Importações necessárias para criar a rota e manipular requisições
from flask import Blueprint
from flask import request
from src.db import medicamentos  # Importa o modelo do banco de dados referente a medicamentos
from src import banco            # Importa a instância do banco de dados
from datetime import datetime    # Importa para manipulação de datas

# Criação de um Blueprint chamado "medicamento" com prefixo de rota "/medicamento"
medicamento = Blueprint("medicamento", __name__, url_prefix="/medicamento")

# Rota para cadastrar um novo medicamento
@medicamento.route("/cadastrar_medicamento", methods=["POST"])
def cadastrar_medicamento():
    # Coleta os dados do formulário enviados na requisição
    nome_medicamento = request.form.get("nome_medicamento")
    principio_ativo = request.form.get("principio_ativo")
    dosagem = request.form.get("dosagem")
    restricao = request.form.get("restricao")
    bula = request.form.get("bula")  # Campo opcional, como a bula pode ser vazia
    indicacoes = request.form.get("indicacoes")
    contra_indicacoes = request.form.get("contra_indicacoes")
    lote = request.form.get("lote")
    data_validade = request.form.get("data_validade")
    fabricante = request.form.get("fabricante")
    preco_unitario = request.form.get("preco_unitario")
    tarja = request.form.get("tarja")  # Tarja vermelha, preta etc.
    id_fornecedor = request.form.get("id_fornecedor")  # Chave estrangeira

    # Converte a data de validade de string para objeto datetime
    data_validade = datetime.strptime(data_validade, "%d/%m/%Y")

    # Validação dos campos obrigatórios
    if not nome_medicamento or not principio_ativo or not dosagem or not restricao or not indicacoes or not contra_indicacoes or not lote or not preco_unitario or not fabricante:
        return {
            "sucess": False,
            "message": "nome_medicamento, nome_principio_ativo, dosagem, restricao, indicacoes, contra_indicacoes, lote, preco_unitario e fabricante são obrigatórios!"
        }, 400

    # Criação da instância de Medicamento com os dados fornecidos
    novo_medicamento = medicamentos.Medicamento(
        nome_medicamento=nome_medicamento,
        principio_ativo=principio_ativo,
        dosagem=dosagem,
        restricao=restricao,
        bula=bula,
        indicacoes=indicacoes,
        contra_indicacoes=contra_indicacoes,
        lote=lote,
        data_validade=data_validade,
        fabricante=fabricante,
        preco_unitario=preco_unitario,
        tarja=tarja,
        id_fornecedor=id_fornecedor
    )

    # Tenta salvar no banco de dados
    try:
        banco.session.add(novo_medicamento)  # Adiciona à sessão
        banco.session.commit()               # Comita a transação
        return {"sucess": True, "message": "Medicamento cadastrado com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()  # Em caso de erro, desfaz a operação
        print(err)  # Exibe o erro no terminal (útil para debug)
        return {"sucess": False, "message": "Falha ao cadastrar o medicamento no banco de dados!"}, 400
