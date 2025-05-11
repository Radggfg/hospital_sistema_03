# Importa os módulos necessários do Flask
from flask import Blueprint
from flask import request
from src import banco  # Conexão com o banco de dados
from src.db import justificativas_ausencias, escalas_trabalhistas # Tabela de justificativas de ausência
from datetime import datetime  # Para manipular datas
from sqlalchemy import select

# Cria um Blueprint para agrupar as rotas relacionadas à justificativa de ausência
justificativa_ausencia = Blueprint("justificativa_ausencia", __name__, url_prefix="/justificativa_ausencia")


# ===========================
# ROTA: Cadastrar justificativa
# ===========================
@justificativa_ausencia.route("/cadastrar_justificativa", methods=["POST"])
def cadastrar_justificativa():
    # Captura os dados do formulário enviado na requisição
    id_profissional = request.form.get("id_profissional")
    data_ausencia = request.form.get("data_ausencia")
    motivo_ausencia = request.form.get("motivo_ausencia")
    status_justificativa = request.form.get("status_justificativa")
    id_escala = request.form.get("id_escala")

    data_ausencia = datetime.strptime(data_ausencia, "%d/%m/%Y %H:%M:%S")

    if not id_profissional or not data_ausencia or not motivo_ausencia or not status_justificativa or not id_escala:
        return{"sucess":False, "message": "Todos os campos são obeigatórios!"}, 400

    nova_justificativa = justificativas_ausencias.Justificativa_ausencia(
            id_profissional = id_profissional,
            data_ausencia = data_ausencia,
            motivo_ausencia = motivo_ausencia,
            status_justificativa = status_justificativa,
            id_escala = id_escala)

    try:
        banco.session.add(nova_justificativa)
        banco.session.commit()
        return{"sucess":True, "message": "Justificativa cadastrada!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao inserir no banco de dados!"}, 400



# ===========================
# ROTA: Listar todas as justificativas
# ===========================
@justificativa_ausencia.route("/listar_justificativa", methods=["GET"])
def listar_justificativas():
    justificativas_query = select(justificativas_ausencias.Justificativa_ausencia.id_justificativa,
                                justificativas_ausencias.Justificativa_ausencia.id_profissional,
                                justificativas_ausencias.Justificativa_ausencia.data_ausencia,
                                justificativas_ausencias.Justificativa_ausencia.motivo_ausencia,
                                justificativas_ausencias.Justificativa_ausencia.status_justificativa,
                                justificativas_ausencias.Justificativa_ausencia.id_escala)
    todas_justificativas = banco.session.execute(justificativas_query).all()
    lista = []
    for justificativa in todas_justificativas:
        data_ausencia = datetime.strftime(justificativa.data_ausencia, "%d/%m/%Y %H:%M:%S")
        lista.append({
            "id_justificativa":justificativa.id_justificativa,
            "id_profissional":justificativa.id_profissional,
            "data_ausencia":data_ausencia,
            "motivo_ausencia":justificativa.motivo_ausencia,
            "status_justificativa":justificativa.status_justificativa,
            "id_escala":justificativa.id_escala
        })
    return{"sucess":True, "todas_justificativas":lista}



# ===========================
# ROTA: Buscar justificativa por ID
# ===========================
@justificativa_ausencia.route("/buscar_justificativa", methods=["GET"])
def buscar_justificativa_id():
    id_justificativa = request.form.get("id_justificativa")
    if not id_justificativa:
        return{"sucess":False, "message": "O id_justificativa é obrigatório!"}, 400
    try:
        todas_justificativas = banco.session.query(justificativas_ausencias.Justificativa_ausencia).where(justificativas_ausencias.Justificativa_ausencia.id_justificativa==id_justificativa).all()
        lista = []
        for just in todas_justificativas:
            data_ausencia = datetime.strftime(just.data_ausencia,  "%d/%m/%Y %H:%M:%S")
            lista.append({
                "id_profissional":just.id_profissional,
                "data_ausencia":data_ausencia,
                "motivo_ausencia":just.motivo_ausencia,
                "status_justificativa":just.status_justificativa,
                "id_escala":just.id_escala
            })
        return{"sucess":True, "todas_justificativas_id": lista}
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Erro ao obter o id_justificativa!"}, 400


# ===========================
# ROTA: Excluir justificativa
# ===========================
@justificativa_ausencia.route("/excluir_justificativa", methods=["DELETE"])
def excluir_justificativa():
    id_justificativa = request.form.get("id_justificativa")

    if not id_justificativa:
        return {"sucess": False, "message": "id_justificativa é obrigatório!"}, 400

    # Busca a justificativa no banco
    query_justificativa = banco.session.query(justificativas_ausencias.Justificativa_ausencia)\
        .filter(justificativas_ausencias.Justificativa_ausencia.id_justificativa == id_justificativa)\
        .first()

    if not query_justificativa:
        return {"sucess": False, "message": "Justificativa não encontrada!"}, 404

    try:
        banco.session.delete(query_justificativa)
        banco.session.commit()
        return {"sucess": True, "message": "Justificativa deletada com sucesso!"}, 200
    except Exception as err:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao deletar justificativa!", "erro": str(err)}, 400
