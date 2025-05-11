# Rotas relacionadas à gestão de leitos e vínculos com pacientes
from flask import Blueprint, request, jsonify
from flask import request
from src import banco
from src.db import leitos, paciente
from sqlalchemy import select
from datetime import datetime

# Define o blueprint para rotas relacionadas a leitos
leito = Blueprint("leito", __name__, url_prefix="/leito")

# Simulação de base de dados em memória (não utilizada no sistema atual)
leitos_base = [
    {"numero": 1, "status": "DISPONIVEL"},
    {"numero": 2, "status": "OCUPADO"},
    {"numero": 3, "status": "RESERVADO"},
]

# Conjunto de status válidos para leitos
STATUS_VALIDOS = {"DISPONIVEL", "OCUPADO", "MANUTENCAO", "RESERVADO"}

# 1. Cadastrar novo leito
@leito.route("/cadastrar_leitos", methods=["POST"])
def cadastrar_leito():
    numero_sala = request.form.get("numero_sala")
    andar_sala = request.form.get("andar_sala")
    tipo_leito = request.form.get("tipo_leito")
    responsavel = request.form.get("responsavel")

    if not numero_sala or not andar_sala or not tipo_leito or not responsavel:
        return{"sucess":False, "message": "num_sala, andar_sala, tipo_leito e responsavel são obrigatórios!"}, 400

    novo_leito = leitos.Leito(
        numero_sala=numero_sala,
        andar_sala=andar_sala,
        tipo_leito=tipo_leito,
        responsavel=responsavel
    )
    try:
        banco.session.add(novo_leito)
        banco.session.commit()
        return{"sucess":True, "message": "Leito cadastrado!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao cadastrar o leito!"}, 400

# 2. Listar todos os leitos cadastrados
@leito.route("/listar_leitos", methods=["GET"])
def listar_leitos():
    leitos_query = select(leitos.Leito.id_leito, leitos.Leito.numero_sala, leitos.Leito.andar_sala, leitos.Leito.status, leitos.Leito.periodo_ocupacao, leitos.Leito.responsavel)
    todos_leitos = banco.session.execute(leitos_query).all()
    lista = []
    for leito in todos_leitos:
        lista.append({
            "id_leito": leito.id_leito,
            "numero_sala": leito.numero_sala,
            "andar_sala": leito.andar_sala,
            "status": leito.status,
            "periodo_ocupacao": leito.periodo_ocupacao,
            "responsavel": leito.responsavel
        })
    return{"sucess":True, "todos_leitos":lista}

# 3. Buscar leito por ID
@leito.route("/buscar_leitos", methods=["GET"])
def buscar_leito_id():
    id_leito = request.form.get("id_leito")
    if not id_leito:
        return{"sucess":False, "message": "O id do leito é obrigatório!"}, 400
    try:
        query_leito = banco.session.query(leitos.Leito).where(leitos.Leito==id_leito).first()
        banco.session.commit()
        return{"sucess":True, "message": "O id do leito foi encontrado!", "leito":query_leito}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao encontrar o id do leito!"}, 400

# 4. Atualizar dados de um leito
@leito.route("/atualizar_status", methods=["PUT"])
def atualizar_status():
    id_leito = request.form.get("id_leito")
    if not id_leito:
        return{"sucess":False, "message": "id_leito é obrigatório!"}, 400

    novo_numero_sala = request.form.get("numero_sala")
    novo_andar_sala = request.form.get("andar_sala")
    novo_tipo_leito = request.form.get("tipo_leito")
    novo_status = request.form.get("status")
    novo_periodo_ocupacao = request.form.get("periodo_ocupacao")
    novo_responsavel = request.form.get("responsavel")

    try:
        query_leito = banco.session.query(leitos.Leito).where(leitos.Leito.id_leito==id_leito).first()
        if novo_numero_sala:
            query_leito.numero_sala = novo_numero_sala
        if novo_andar_sala:
            query_leito.andar_sala = novo_andar_sala
        if novo_tipo_leito:
            query_leito.tipo_leito = novo_tipo_leito
        if novo_status:
            query_leito.status = novo_status
        if novo_periodo_ocupacao:
            query_leito.periodo_ocupacao = novo_periodo_ocupacao
        if novo_responsavel:
            query_leito.responsavel = novo_responsavel
        banco.session.commit()
        return{"sucess":True, "message": "Dados do leito atualizados com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "id_leito não cadastrado no banco de dados!"}, 400

# 5. Deletar leito
@leito.route("/deletar_leito", methods=["DELETE"])
def deletar_leito():
    id_leito = request.form.get("id_leito")
    query_leito = banco.session.query(leitos.Leito).where(leitos.Leito.id_leito==id_leito).first()
    try:
        banco.session.delete(query_leito)
        banco.session.commit()
        return{"sucess":True, "message": "Leito deletado com sucesso!"}, 201
    except Exception as err:
        print(err)
        return{"sucess":False, "message": "Falha ao deletar o leito!"}, 400

# 6. Criar vínculo entre paciente e leito (internação)
@leito.route('/criar_paciente_leito', methods=['POST'])
def criar_paciente_leito():
    id_paciente = request.form.get("id_paciente")
    id_leito = request.form.get("id_leito")
    data_internacao = request.form.get("data_internacao")
    status = request.form.get("status")

    data_internacao = datetime.strptime(data_internacao, "%d/%m/%Y %H:%M:%S")

    if not id_paciente or not id_leito or not data_internacao or not status:
        return{"sucess":False, "message": "id_paciente, id_leito, data_internacao e status são obrigatórios!"}, 400

    novo_paciente_leito = paciente.Paciente_Leito(
        id_paciente=id_paciente,
        id_leito=id_leito,
        data_internacao=data_internacao,
        status=status
    )

    try:
        banco.session.add(novo_paciente_leito)
        banco.session.commit()
        return{"sucess":True, "message": "Paciente_leito cadastrado com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao cadastrar o paciente_leito!"}, 400

# 7. Listar todos os vínculos paciente-leito
@leito.route('/listar_paciente_leito', methods=['GET'])
def listar_pacientes_leitos():
    paciente_leito_query = select(
        paciente.Paciente_Leito.id_paciente_leito,
        paciente.Paciente_Leito.id_paciente,
        paciente.Paciente_Leito.id_leito,
        paciente.Paciente_Leito.data_internacao,
        paciente.Paciente_Leito.data_alta,
        paciente.Paciente_Leito.status
    )
    todos_pacientes_leitos = banco.session.execute(paciente_leito_query).all()
    lista = []
    for pacinte_leito in todos_pacientes_leitos:
        lista.append({
            "id_paciente_leito": pacinte_leito.id_paciente_leito,
            "id_paciente": pacinte_leito.id_paciente,
            "id_leito": pacinte_leito.id_leito,
            "id_data_internacao": pacinte_leito.data_internacao,
            "data_alta": pacinte_leito.data_alta,
            "status": pacinte_leito.status,
        })
    return{"sucess":True, "todos_pacientes_leitos": lista}

# 8. Obter um vínculo específico
@leito.route('/obter_paciente_leito', methods=['GET'])
def obter_paciente_leito():
    id_paciente_leito = request.form.get("id_paciente_leito")
    if not id_paciente_leito:
        return{"sucess":False, "message": "id_paciente_leito é obrigatório!"}, 400

    query_obter_paciente_leito = banco.session.query(paciente.Paciente_Leito).where(paciente.Paciente_Leito.id_paciente_leito==id_paciente_leito).first()
    if not query_obter_paciente_leito:
        return{"sucess":False, "message": "id_paciente_leito não existe!"}, 400

    return{"sucess":True, "message": "id_paciente_leito foi encontrado!",
        "id_paciente": query_obter_paciente_leito.id_paciente,
        "id_leito": query_obter_paciente_leito.id_leito,
        "data_internacao": query_obter_paciente_leito.data_internacao,
        "data_alta": query_obter_paciente_leito.data_alta,
        "status": query_obter_paciente_leito.status,
        "observacoes": query_obter_paciente_leito.observacoes}, 201

# 9. Atualizar dados de um vínculo paciente-leito
@leito.route('/atualizar_paciente_leito', methods=['PUT'])
def atualizar_paciente_leito():
    id_paciente_leito = request.form.get("id_paciente_leito")
    if not id_paciente_leito:
        return{"sucess":False, "message": "id_paciente_leito é obrigatório!"}, 400

    novo_id_paciente = request.form.get("id_paciente")
    novo_id_leito = request.form.get("id_leito")
    nova_data_internacao = request.form.get("data_internacao")
    nova_data_alta = request.form.get("data_alta")
    novo_status = request.form.get("status")
    novas_observacoes = request.form.get("observacoes")

    try:
        query_paciente_leito = banco.session.query(paciente.Paciente_Leito).where(paciente.Paciente_Leito.id_paciente_leito==id_paciente_leito).first()
        if novo_id_paciente:
            query_paciente_leito.id_paciente = novo_id_paciente
        if novo_id_leito:
            query_paciente_leito.id_leito = novo_id_leito
        if nova_data_alta:
            nova_data_alta = datetime.strptime(nova_data_alta, "%d/%m/%Y")
            query_paciente_leito.data_alta = nova_data_alta
        if nova_data_internacao:
            nova_data_internacao = datetime.strptime(nova_data_internacao, "%d/%m/%Y")
            query_paciente_leito.data_internacao = nova_data_internacao
        if novo_status:
            query_paciente_leito.status = novo_status
        if novas_observacoes:
            query_paciente_leito.observacoes = novas_observacoes
        banco.session.commit()
        return{"sucess":True, "message": "Dados do paciente_leito atualizados com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao atualizar os dados do paciente_leito!"}, 400

# 10. Deletar vínculo paciente-leito
@leito.route('/deletar_paciente_leito', methods=['DELETE'])
def deletar_paciente_leito():
    id_paciente_leito = request.form.get("id_paciente_leito")
    query_paciente_leito = banco.session.query(paciente.Paciente_Leito).where(paciente.Paciente_Leito.id_paciente_leito==id_paciente_leito).first()
    try:
        banco.session.delete(query_paciente_leito)
        banco.session.commit()
        return{"sucess":True, "message": "Paciente_leito deletado com sucesso!"}, 201
    except Exception as err:
        print(err)
        return{"sucess":False, "message": "Falha ao deletar o Paciente_leito!"}, 400
