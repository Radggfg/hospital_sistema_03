from flask import Blueprint, request
from src import banco
from src.db import escalas_trabalhistas
from datetime import datetime
from sqlalchemy import select

# Criação dos blueprints para as rotas da escala e fluxo de horário
escala_trabalhista = Blueprint("escala_trabalhista", __name__, url_prefix="/escala_trabalhista")
fluxo_horario = Blueprint("fluxo_horario", __name__, url_prefix="/fluxo_horario")

# Rota para cadastrar uma nova escala trabalhista
@escala_trabalhista.route("/cadastrar_escala", methods=["POST"])
def cadastrar_escala():
    id_profissional = request.form.get("id_profissional")
    periodo_escala = request.form.get("periodo_escala")
    periodo_inicio = request.form.get("periodo_inicio")
    periodo_fim = request.form.get("periodo_fim")
    tipo_turno = request.form.get("tipo_turno")
    id_setor = request.form.get("id_setor")

    periodo_escala = datetime.strptime(periodo_escala, "%d/%m/%Y %H:%M:%S")
    periodo_inicio = datetime.strptime(periodo_inicio, "%H:%M")
    periodo_fim = datetime.strptime(periodo_fim, "%H:%M")

    # Verifica se todos os campos obrigatórios foram preenchidos
    if not id_profissional or not periodo_escala or not periodo_inicio or not periodo_fim or not tipo_turno or not id_setor:
        return{"sucess":False, "message": "Todos os campos são obrigatórios!"}, 400

    nova_escala = escalas_trabalhistas.Escala_Trabalhista(
        id_profissional=id_profissional,
        periodo_escala=periodo_escala,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
        tipo_turno=tipo_turno,
        id_setor=id_setor)

    try:
        banco.session.add(nova_escala)
        banco.session.commit()
        return {"success": True, "message": "Escala cadastrada com sucesso."}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"success": False, "message": "Erro ao cadastrar escala!"}, 400

# Rota para listar todas as escalas cadastradas
@escala_trabalhista.route("/listar_escala", methods=["GET"])
def listar_escalas():
    escala_query = select(
        escalas_trabalhistas.Escala_Trabalhista.id_profissional,
        escalas_trabalhistas.Escala_Trabalhista.periodo_escala,
        escalas_trabalhistas.Escala_Trabalhista.periodo_inicio,
        escalas_trabalhistas.Escala_Trabalhista.periodo_fim,
        escalas_trabalhistas.Escala_Trabalhista.tipo_turno,
        escalas_trabalhistas.Escala_Trabalhista.id_setor,
        escalas_trabalhistas.Escala_Trabalhista.id_escala
    )

    todas_escalas = banco.session.execute(escala_query).all()
    lista = []
    for escala in todas_escalas:
        inicio_hora = f"{escala.periodo_inicio.hour}:{escala.periodo_inicio.minute:02}"
        fim_hora = f"{escala.periodo_fim.hour}:{escala.periodo_fim.minute:02}"
        time = datetime.strftime(escala.periodo_escala, "%d/%m/%Y")
        lista.append({
            "id_profissional": escala.id_profissional,
            "periodo_escala": time,
            "periodo_inicio": inicio_hora,
            "periodo_fim": fim_hora,
            "tipo_turno": escala.tipo_turno,
            "id_setor": escala.id_setor,
            "id_escala": escala.id_escala,
        })
    return{"sucess":True, "todas_escalas": lista}

# Rota para buscar uma escala específica por ID
@escala_trabalhista.route("/buscar_escala_id", methods=["GET"])
def buscar_escala_id():
    id_escala = request.form.get("id_escala")
    if not id_escala:
        return {"sucess": False, "message": "Escala é obrigatório!"}, 400
    try:
        todas_escalas = banco.session.query(escalas_trabalhistas.Escala_Trabalhista).where(escalas_trabalhistas.Escala_Trabalhista.id_escala==id_escala).all()
        lista = []
        for escala in todas_escalas:
            inicio_hora = f"{escala.periodo_inicio.hour}:{escala.periodo_inicio.minute:02}"
            fim_hora = f"{escala.periodo_fim.hour}:{escala.periodo_fim.minute:02}"
            time = datetime.strftime(escala.periodo_escala, "%d/%m/%Y")
            lista.append({
                "id_profissional":escala.id_profissional,
                "periodo_escala":time,
                "periodo_inicio":inicio_hora,
                "periodo_fim":fim_hora,
                "tipo_turno":escala.tipo_turno,
                "id_setor":escala.id_setor,
                "id_escala":escala.id_escala
            })
            return {"sucess": True, "todas_escalas": lista}
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Erro ao buscar por escala."}, 400

# Rota para atualizar os dados de uma escala
@escala_trabalhista.route("/atualizar_escala", methods=["PUT"])
def atualizar_escala():
    id_escala = request.form.get("id_escala")
    if not id_escala:
        return{"sucess":False, "message": "id_escala é obrigatório!"}, 400
    novo_periodo = request.form.get("periodo_escala")
    novo_inicio = request.form.get("periodo_inicio")
    novo_fim = request.form.get("periodo_fim")
    novo_turno = request.form.get("tipo_turno")
    novo_setor = request.form.get("id_setor")
    novo_periodo = datetime.strptime(novo_periodo, "%d/%m/%Y  %H:%M:%S")
    try:
        query_escala = banco.session.query(escalas_trabalhistas.Escala_Trabalhista).where(escalas_trabalhistas.Escala_Trabalhista.id_escala==id_escala).first()
        if novo_periodo:
            query_escala.periodo_escala = novo_periodo
        if novo_inicio:
            query_escala.periodo_inicio = novo_inicio
        if novo_fim:
            query_escala.periodo_fim = novo_fim
        if novo_turno:
            query_escala.tipo_turno = novo_turno
        if novo_setor:
            query_escala.id_setor = novo_setor
        banco.session.commit()
        return{"sucess":True, "message": "Dados da escala atualizados com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao atualizar os dados da escala!"}, 400

# Rota para deletar uma escala específica
@escala_trabalhista.route("/excluir_escala", methods=["DELETE"])
def excluir_escala():
    id_escala = request.form.get("id_escala")
    query_escala = banco.session.query(escalas_trabalhistas.Escala_Trabalhista).filter_by(id_escala=id_escala).first()
    try:
        banco.session.delete(query_escala)
        banco.session.commit()
        return{"sucess":True, "message": "Escala deletada com sucesso!"}, 201
    except Exception as err:
        print(err)
        return{"sucess":False, "message": "Falha ao deletar a escala!"}, 400

# Rota para criar um novo fluxo de horário
@fluxo_horario.route('/criar_fluxo_horario', methods=['POST'])
def criar_fluxo_horario():
    id_profissional = request.form.get("id_profissional")
    data_movimentacao = request.form.get("data_movimentacao")
    hora_entrada = request.form.get("hora_entrada")
    hora_saida = request.form.get("hora_saida")
    id_setor = request.form.get("id_setor")
    id_escala = request.form.get("id_escala")

    data_movimentacao = datetime.strptime(data_movimentacao, "%d/%m/%Y")
    hora_entrada = datetime.strptime(hora_entrada, "%H:%M:%S")
    hora_saida = datetime.strptime(hora_saida, "%H:%M:%S")

    if not id_profissional or not data_movimentacao or not  hora_entrada or not hora_saida or not id_setor or not id_escala:
        return {"success": False, "message": "Todos os campos são obrigatórios!"}, 400

    novo_fluxo = escalas_trabalhistas.Fluxo_Horario(
        data_movimentacao=data_movimentacao,
        id_profissional=id_profissional,
        hora_entrada=hora_entrada,
        hora_saida=hora_saida,
        id_setor=id_setor,
        id_escala=id_escala
    )

    try:
        banco.session.add(novo_fluxo)
        banco.session.commit()
        return {"success": True, "message": "Fluxo criado com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"success": False, "message": "Erro ao criar fluxo.", "erro": str(err)}, 500

# Rota para listar todos os fluxos cadastrados
@fluxo_horario.route('/listar_fluxo_horario', methods=['GET'])
def listar_fluxos():
    fluxo_query = select(
        escalas_trabalhistas.Fluxo_Horario.id_profissional,
        escalas_trabalhistas.Fluxo_Horario.data_movimentacao,
        escalas_trabalhistas.Fluxo_Horario.hora_entrada,
        escalas_trabalhistas.Fluxo_Horario.hora_saida,
        escalas_trabalhistas.Fluxo_Horario.id_setor,
        escalas_trabalhistas.Fluxo_Horario.id_escala
        )
    todos_fluxos = banco.session.execute(fluxo_query).all()
    lista = []
    for fluxo in todos_fluxos: 
        data_movimentacao = datetime.strftime(fluxo.data_movimentacao, "%d/%m/%Y")
        hora_entrada = f"{fluxo.hora_entrada.hour}:{fluxo.hora_entrada.minute:02}"
        hora_saida = f"{fluxo.hora_saida.hour}:{fluxo.hora_saida.minute:02}"
        lista.append({
            "id_profissional": fluxo.id_profissional,
            "data_movimentacao": data_movimentacao,
            "hora_entrada": hora_entrada,
            "hora_saida": hora_saida,
            "id_setor": fluxo.id_setor,
            "id_escala": fluxo.id_escala,
        })
    return{"sucess":True, "todos_fluxos":lista}





# Rota para obter informações de um fluxo específico por ID
@fluxo_horario.route('/obter_fluxo_horario', methods=['GET'])
def obter_fluxo():
    id_fluxo = request.form.get("id_fluxo")
    if not id_fluxo:
        return{"sucess":False, "message": "id_fluxo é obrigatório!"}, 400
    query_fluxo = banco.session.query(escalas_trabalhistas.Fluxo_Horario).filter_by(id_fluxo=id_fluxo).all()
    if not query_fluxo:
        return{"sucess":False, "message": "Id do fluxo não existe!"}, 400
    lista = []
    for fluxo in query_fluxo:
        data_movimentacao = datetime.strftime(fluxo.data_movimentacao, "%d/%m/%Y")
        hora_entrada = f"{fluxo.hora_entrada.hour}:{fluxo.hora_entrada.minute:02}"
        hora_saida = f"{fluxo.hora_saida.hour}:{fluxo.hora_saida.minute:02}"
        lista.append({
            "id_profissional": fluxo.id_profissional,
            "data_movimentacao": data_movimentacao,
            "hora_entrada": hora_entrada,
            "hora_saida": hora_saida,
            "id_setor": fluxo.id_setor,
            "id_escala": fluxo.id_escala,
        })
    return{"sucess":True, "todos_fluxos":lista}




# Rota para atualizar dados de um fluxo de horário
@fluxo_horario.route('/atualizar_fluxo_horario', methods=['PUT'])
def atualizar_fluxo():
    id_fluxo = request.form.get("id_fluxo")
    if not id_fluxo:
        return{"sucess":False, "message": "id_fluxo é obrigatório!"}, 400
    nova_hora_entrada = request.form.get("hora_entrada")
    nova_hora_saida = request.form.get("hora_saida")
    try:
        query_fluxo = banco.session.query(escalas_trabalhistas.Fluxo_Horario).where(escalas_trabalhistas.Fluxo_Horario.id_fluxo==id_fluxo).first()
        if nova_hora_entrada:
            query_fluxo.hora_entrada = nova_hora_entrada
        if nova_hora_saida:
            query_fluxo.hora_saida = nova_hora_saida
        banco.session.commit()
        return{"sucess":True, "message": "Dados do fluxo atualizados com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao atualizar os dados do fluxo!"}, 400



# Rota para deletar um fluxo de horário por ID
@fluxo_horario.route('/deletar_fluxo_horario', methods=['DELETE'])
def deletar_fluxo():
    id_fluxo = request.form.get("id_fluxo")
    query_fluxo = banco.session.query(escalas_trabalhistas.Fluxo_Horario).filter_by(id_fluxo=id_fluxo).first()
    try:
        banco.session.delete(query_fluxo)
        banco.session.commit()
        return{"sucess":True, "message": "Fluxo deletado com sucesso!"}, 201
    except Exception as err:
        return{"sucess":False, "message": "Falha ao deletar o fluxo!"}, 400
