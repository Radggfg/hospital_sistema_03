from flask import Blueprint, request  # Importa os recursos do Flask para criação de rotas e leitura de dados
from src import banco  # Importa a instância de banco de dados
from src.db import diagnosticos  # Importa o modelo Diagnostico
from datetime import datetime  # (Importado mas não usado nesse código)
from sqlalchemy import select  # Para consultas estruturadas via SQLAlchemy

# Criação do Blueprint para as rotas de diagnóstico
diagnostico = Blueprint("diagnostico", __name__, url_prefix="/diagnostico")

# ---------------------------- CRIAR DIAGNÓSTICO ----------------------------
@diagnostico.route('/criar_diagnostico', methods=['POST'])
def criar_diagnostico():
    tipo_sanguineo = request.form.get("tipo_sanguineo")
    descricao = request.form.get("descricao")

    # Validação de campos obrigatórios
    if not tipo_sanguineo or not descricao:
        return {"sucess": False, "message": "tipo_sanguineo e descricao são obrigatórios!"}, 400

    # Criação do novo objeto Diagnostico
    novo_diagnostico = diagnosticos.Diagnostico(
        tipo_sanguineo=tipo_sanguineo,
        descricao=descricao
    )

    try:
        banco.session.add(novo_diagnostico)
        banco.session.commit()
        return {"sucess": True, "message": "Diagnóstico agendado com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao agendar o diagnóstico!"}, 400

# ---------------------------- LISTAR DIAGNÓSTICOS ----------------------------
@diagnostico.route('/listar_diagnostico', methods=['GET'])
def listar_diagnosticos():
    # Consulta para selecionar todos os diagnósticos
    diagnosticos_query = select(
        diagnosticos.Diagnostico.id_diagnostico,
        diagnosticos.Diagnostico.tipo_sanguineo,
        diagnosticos.Diagnostico.descricao
    )
    todos_diagnosticos = banco.session.execute(diagnosticos_query).all()

    # Transforma resultados em lista de dicionários
    lista = []
    for diag in todos_diagnosticos:
        lista.append({
            "id_diagnostico": diag.id_diagnostico,
            "tipo_sanguineo": diag.tipo_sanguineo,
            "descricao": diag.descricao
        })
    return {"sucess": True, "todos_diagnosticos": lista}

# ---------------------------- OBTER DIAGNÓSTICO POR ID ----------------------------
@diagnostico.route('/obter_diagnostico', methods=['GET'])
def obter_diagnostico():
    id_diagnostico = request.form.get("id_diagnostico")
    if not id_diagnostico:
        return {"sucess": False, "message": "id_diagnostico é obrigatório!"}, 400

    # Busca o diagnóstico pelo ID
    query = banco.session.query(diagnosticos.Diagnostico).where(
        diagnosticos.Diagnostico.id_diagnostico == id_diagnostico
    ).first()

    if not query:
        return {"sucess": False, "message": "id_diagnostico não existe!"}, 400

    # Retorna os dados do diagnóstico
    return {
        "sucess": True,
        "message": "id_diagnostico foi encontrado!",
        "tipo_sanguineo": query.tipo_sanguineo,
        "descricao": query.descricao
    }, 201

# ---------------------------- ATUALIZAR DIAGNÓSTICO ----------------------------
@diagnostico.route('/atualizar_diagnostico', methods=['PUT'])
def atualizar_diagnostico():
    id_diagnostico = request.form.get("id_diagnostico")
    if not id_diagnostico:
        return {"sucess": False, "message": "id_diagnostico é obrigatório!"}, 400

    nova_descricao = request.form.get("descricao")

    try:
        # Busca o diagnóstico a ser atualizado
        query = banco.session.query(diagnosticos.Diagnostico).where(
            diagnosticos.Diagnostico.id_diagnostico == id_diagnostico
        ).first()

        # Atualiza o campo se fornecido
        if nova_descricao:
            query.descricao = nova_descricao

        banco.session.commit()
        return {"sucess": True, "message": "Dados do diagnóstico atualizados com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao atualizar os dados do diagnóstico!"}, 400
