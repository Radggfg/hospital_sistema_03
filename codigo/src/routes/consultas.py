from flask import Blueprint, request  # Importa os módulos necessários do Flask
from src import banco  # Sessão do banco de dados
from src.db import consultas  # Importa o modelo Consulta
from datetime import datetime  # Para manipular datas e horários
from sqlalchemy import select  # Para construir consultas SQL de forma segura

# Criação do Blueprint para rotas relacionadas a consultas
consulta = Blueprint("consulta", __name__, url_prefix="/consulta")

# ---------------------------- CRIAR CONSULTA ----------------------------
@consulta.route('/criar_consulta', methods=['POST'])
def criar_consulta():
    # Coleta os dados do formulário
    id_paciente = request.form.get("id_paciente")
    id_profissional = request.form.get("id_profissional")
    data_hora = request.form.get("data_hora")
    prescricao = request.form.get("prescricao")
    tipo_consulta = request.form.get("tipo_consulta")

    # Valida campos obrigatórios
    if not id_paciente or not id_profissional or not data_hora or not prescricao or not tipo_consulta:
        return {"sucess": False, "message": "Campos obrigatórios faltando!"}, 400

    # Converte data e hora de string para objeto datetime
    data_hora = datetime.strptime(data_hora, "%d/%m/%Y %H:%M")

    # Cria objeto de consulta
    nova_consulta = consultas.Consulta(
        id_paciente=id_paciente,
        id_profissional=id_profissional,
        data_hora=data_hora,
        prescricao=prescricao,
        tipo_consulta=tipo_consulta
    )

    try:
        banco.session.add(nova_consulta)
        banco.session.commit()
        return {"sucess": True, "message": "Consulta agendada com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao agendar a consulta!"}, 400

# ---------------------------- LISTAR CONSULTAS ----------------------------
@consulta.route('/listar_consulta', methods=['GET'])
def listar_consultas():
    # Consulta todos os registros da tabela Consulta
    consultas_query = select(
        consultas.Consulta.id_consulta,
        consultas.Consulta.id_paciente,
        consultas.Consulta.id_profissional,
        consultas.Consulta.data_hora,
        consultas.Consulta.id_diagnostico,
        consultas.Consulta.prescricao,
        consultas.Consulta.tipo_consulta,
        consultas.Consulta.id_prontuario,
        consultas.Consulta.id_exame,
        consultas.Consulta.id_faturamento_hospitalar
    )
    todas_consultas = banco.session.execute(consultas_query).all()

    # Transforma resultado em lista de dicionários
    lista = []
    for agendamento in todas_consultas:
        lista.append({
            "id_consulta": agendamento.id_consulta,
            "id_paciente": agendamento.id_paciente,
            "id_profissional": agendamento.id_profissional,
            "data_hora": agendamento.data_hora,
            "id_diagnostico": agendamento.id_diagnostico,
            "prescricao": agendamento.prescricao,
            "tipo_consulta": agendamento.tipo_consulta,
            "id_prontuario": agendamento.id_prontuario,
            "id_exame": agendamento.id_exame,
            "id_faturamento_hospitalar": agendamento.id_faturamento_hospitalar
        })
    return {"sucess": True, "todas_consultas": lista}

# ---------------------------- CONSULTA POR ID ----------------------------
@consulta.route('/obter_consulta', methods=['GET'])
def obter_consulta():
    id_consulta = request.form.get("id_consulta")
    if not id_consulta:
        return {"sucess": False, "message": "id_consulta é obrigatório!"}, 400

    # Busca consulta por ID
    query_consulta = banco.session.query(consultas.Consulta).where(consultas.Consulta.id_consulta == id_consulta).first()
    if not query_consulta:
        return {"sucess": False, "message": "Id da consulta não existe!"}, 400

    # Retorna dados da consulta
    return {
        "sucess": True,
        "message": "Consulta encontrada!",
        "id_paciente": query_consulta.id_paciente,
        "id_profissional": query_consulta.id_profissional,
        "data_hora": query_consulta.data_hora,
        "id_diagnostico": query_consulta.id_diagnostico,
        "prescricao": query_consulta.prescricao,
        "tipo_consulta": query_consulta.tipo_consulta,
        "id_prontuario": query_consulta.id_prontuario,
        "id_exame": query_consulta.id_exame,
        "id_faturamento_hospitalar": query_consulta.id_faturamento_hospitalar
    }, 201

# ---------------------------- ATUALIZAR CONSULTA ----------------------------
@consulta.route('/atualizar_consulta', methods=['PUT'])
def atualizar_consulta():
    id_consulta = request.form.get("id_consulta")
    if not id_consulta:
        return {"sucess": False, "message": "id_consulta é obrigatório!"}, 400

    # Coleta possíveis dados atualizáveis
    nova_data_hora = request.form.get("data_hora")
    novo_id_profissional = request.form.get("id_profissional")
    novo_id_diagnostico = request.form.get("id_diagnostico")
    nova_prescricao = request.form.get("prescricao")
    novo_tipo_consulta = request.form.get("tipo_consulta")
    novo_id_faturamento_hospitalar = request.form.get("id_faturamento_hospitalar")

    try:
        # Busca consulta existente
        query_consulta = banco.session.query(consultas.Consulta).where(consultas.Consulta.id_consulta == id_consulta).first()

        # Atualiza os campos recebidos
        if nova_data_hora:
            query_consulta.data_hora = datetime.strptime(nova_data_hora, "%d/%m/%Y %H:%M")
        if novo_id_profissional:
            query_consulta.id_profissional = novo_id_profissional
        if novo_id_diagnostico:
            query_consulta.id_diagnostico = novo_id_diagnostico
        if nova_prescricao:
            query_consulta.prescricao = nova_prescricao
        if novo_tipo_consulta:
            query_consulta.tipo_consulta = novo_tipo_consulta
        if novo_id_faturamento_hospitalar:
            query_consulta.id_faturamento_hospitalar = novo_id_faturamento_hospitalar

        banco.session.commit()
        return {"sucess": True, "message": "Consulta atualizada com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao atualizar a consulta!"}, 400





