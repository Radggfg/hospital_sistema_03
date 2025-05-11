from flask import Blueprint, request
from src import banco
from src.db import despesas_hospitalares, paciente

# Cria o Blueprint para o módulo financeiro
financeiro = Blueprint('financeiro', __name__, url_prefix="/financeiro")

# Endpoint para criar uma nova despesa hospitalar
@financeiro.route('/criar_despesa', methods=['POST'])
def criar_despesa():
    id_medicamento = request.form.get("id_medicamento")
    id_equipamento = request.form.get("id_equipamento")
    id_salario_profissional = request.form.get("id_salario_profissional")
    valor_total = request.form.get("valor_total")
    id_pagamento = request.form.get("id_pagamento")
    id_tipo_pagamento = request.form.get("id_tipo_pagamento")
    id_leito = request.form.get("id_leito")
    id_procedimento = request.form.get("id_procedimento")
    id_consulta = request.form.get("id_consulta")
    id_fornecedor = request.form.get("id_fornecedor")
    data_despesa = request.form.get("data_despesa")
    id_exame = request.form.get("id_exame")

    if not all([id_medicamento, id_equipamento, id_salario_profissional, valor_total, id_pagamento,
                id_tipo_pagamento, id_leito, id_procedimento, id_consulta, id_fornecedor, data_despesa, id_exame]):
        return {"sucess": False, "message": "Todos os campos são obrigatórios!"}, 400

    nova_despesa = despesas_hospitalares.Despesa_Hospitalar(
        id_medicamento=id_medicamento,
        id_equipamento=id_equipamento,
        id_salario_profissional=id_salario_profissional,
        valor_total=valor_total,
        id_pagamento=id_pagamento,
        id_tipo_pagamento=id_tipo_pagamento,
        id_leito=id_leito,
        id_procedimento=id_procedimento,
        id_consulta=id_consulta,
        id_fornecedor=id_fornecedor,
        data_despesa=data_despesa,
        id_exame=id_exame
    )

    try:
        banco.session.add(nova_despesa)
        banco.session.commit()
        return {"sucess": True, "message": "Despesa registrada com sucesso!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao registrar a despesa!"}, 400

# Endpoint para listar todas as despesas
@financeiro.route('/listar_despesa', methods=['GET'])
def listar_despesas():
    todas_despesas = despesas_hospitalares.Despesa_Hospitalar.query.all()
    return {"sucess": True, "todas_despesas": todas_despesas}

# Endpoint para listar despesas por paciente (aqui é preciso revisar a lógica de consulta)
@financeiro.route('/listar_despesa_paciente', methods=['GET'])
def listar_despesas_por_paciente():
    id_paciente = request.form.get("id_paciente")
    try:
        query_despesa = banco.session.query(paciente.Paciente).where(paciente.Paciente.cpf == id_paciente).all()
        if not query_despesa:
            return {"sucess": False, "message": "Nenhuma despesa encontrada!"}, 400
        return {"sucess": True, "message": "Despesas encontradas!", "listar_despesas_por_paciente": query_despesa}, 201
    except Exception:
        return {"sucess": False, "message": "Erro na consulta de despesas."}, 400

# Endpoint para obter uma despesa específica
@financeiro.route('/obter_despesa', methods=['GET'])
def obter_despesa():
    id_despesa_hospitalar = request.form.get("id_despesa_hospitalar")
    if not id_despesa_hospitalar:
        return {"sucess": False, "message": "id_despesa_hospitalar é obrigatório!"}, 400
    query_despesa = banco.session.query(despesas_hospitalares.Despesa_Hospitalar).where(
        despesas_hospitalares.Despesa_Hospitalar.id_despesa_hospitalar == id_despesa_hospitalar).first()
    if not query_despesa:
        return {"sucess": False, "message": "Despesa não encontrada!"}, 400
    return {"sucess": True, "despesa": query_despesa}, 201

# Endpoint para atualizar uma despesa
@financeiro.route('/atualizar_despesa', methods=['PUT'])
def atualizar_despesa():
    id_despesa_hospitalar = request.form.get("id_despesa_hospitalar")
    if not id_despesa_hospitalar:
        return {"sucess": False, "message": "id_despesa_hospitalar é obrigatório!"}, 400
    novo_valor_total = request.form.get("valor_total")
    novo_id_tipo_pagamento = request.form.get("id_tipo_pagamento")
    try:
        query_despesa = banco.session.query(despesas_hospitalares.Despesa_Hospitalar).where(
            despesas_hospitalares.Despesa_Hospitalar.id_despesa_hospitalar == id_despesa_hospitalar).first()
        if novo_valor_total:
            query_despesa.valor_total = novo_valor_total
        if novo_id_tipo_pagamento:
            query_despesa.id_tipo_pagamento = novo_id_tipo_pagamento
        banco.session.commit()
        return {"sucess": True, "message": "Despesa atualizada com sucesso!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao atualizar a despesa!"}, 400

# Endpoint para deletar uma despesa
@financeiro.route('/deletar_despesa', methods=['DELETE'])
def deletar_despesa():
    id_despesa_hospitalar = request.form.get("id_despesa_hospitalar")
    query_despesa = banco.session.query(despesas_hospitalares.Despesa_Hospitalar).where(
        despesas_hospitalares.Despesa_Hospitalar.id_despesa_hospitalar == id_despesa_hospitalar).first()
    try:
        banco.session.delete(query_despesa)
        banco.session.commit()
        return {"sucess": True, "message": "Despesa deletada com sucesso!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao deletar a despesa!"}, 400
