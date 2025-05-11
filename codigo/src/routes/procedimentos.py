# Rotas relacionadas a procedimentos, especialidades e tipos de procedimentos
from flask import Blueprint, request, jsonify
from src import banco
from src.db import procedimentos, especialidades, tipos_procedimentos
from datetime import datetime
from sqlalchemy import select
from decimal import Decimal
from decimal import Decimal, InvalidOperation
import re



# Blueprints de rotas
procedimento = Blueprint("procedimento",__name__,url_prefix = "/procedimento")
especialidade = Blueprint("especialidade",__name__,url_prefix = "/especialidade")
tipo_procedimento = Blueprint("tipo_procedimento",__name__,url_prefix = "/tipo_procedimento")

# Criar novo procedimento
@procedimento.route('/criar_procedimento', methods=['POST'])
def criar_procedimento():
    # Recebe dados do formulário
    id_paciente = request.form.get("id_paciente")
    id_profissional = request.form.get("id_profissional")
    data_procedimento = request.form.get("data_procedimento")
    id_especialidade = request.form.get("id_especialidade")

    # Validação básica
    if not id_paciente or not id_profissional or not data_procedimento or not id_especialidade:
        return{"sucess":False, "message": "id_paciente, id_profissional, data_procedimento, id_especialidade são obrigatórios!"}, 400

    data_procedimento = datetime.strptime(data_procedimento, "%d/%m/%Y %H:%M")

    novo_procedimento = procedimentos.Procedimento(
        id_paciente = id_paciente,
        id_profissional = id_profissional,
        data_procedimento = data_procedimento,
        id_especialidade = id_especialidade
    )

    try:
        banco.session.add(novo_procedimento)
        banco.session.commit()
        return{"sucess":True, "message": "Procedimento agendado com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao agendar o procedimento !"}, 400


# Listar todos os procedimentos
@procedimento.route('/listar_procedimento', methods=['GET'])
def listar_procedimentos():
    procedimentos_query = select(
        procedimentos.Procedimento.id_procedimento,
        procedimentos.Procedimento.id_paciente,
        procedimentos.Procedimento.id_profissional,
        procedimentos.Procedimento.data_procedimento,
        procedimentos.Procedimento.id_especialidade,
        procedimentos.Procedimento.id_recebimento_paciente,
        procedimentos.Procedimento.id_despesa_hospitalar,
        procedimentos.Procedimento.id_tipo_procedimento,
        procedimentos.Procedimento.id_equipamento
    )
    todos_procedimentos = banco.session.execute(procedimentos_query).all()
    lista = []
    for processo in todos_procedimentos:
        lista.append({
            "id_procedimento":processo.id_procedimento,
            "id_paciente":processo.id_paciente,
            "id_profissional":processo.id_profissional,
            "data_procedimento":processo.data_procedimento,
            "id_especialidade":processo.id_especialidade,
            "id_recebimento_paciente":processo.id_recebimento_paciente,
            "id_despesa_hospitalar":processo.id_despesa_hospitalar,
            "id_tipo_procedimento":processo.id_tipo_procedimento,
            "id_equipamento":processo.id_equipamento
        })
    return{"sucess":True, "todos_procedimentos":lista}


# Obter um procedimento específico
@procedimento.route('/obter_procedimento', methods=['GET'])
def obter_procedimento():
    id_procedimento = request.form.get("id_procedimento")
    if not id_procedimento:
        return{"sucess":False, "message": "id_procedimento é obrigatório!"}, 400
    query_procedimento = banco.session.query(procedimentos.Procedimento).where(procedimentos.Procedimento.id_procedimento==id_procedimento).first()
    if not query_procedimento:
        return{"sucess":False, "message": "Id do procedimento não existe!"}, 400
    return{"sucess":True, "message": "Id do procedimento foi encontrado!",
        "id_paciente": query_procedimento.id_paciente,
        "id_profissional": query_procedimento.id_profissional,
        "data_procedimento": query_procedimento.data_procedimento,
        "id_especialidade": query_procedimento.id_especialidade,
        "id_tipo_procedimento": query_procedimento.id_tipo_procedimento,
        "id_equipamento": query_procedimento.id_equipamento}, 201


# Atualizar um procedimento existente
@procedimento.route('/atualizar_procedimento', methods=['PUT'])
def atualizar_procedimento():
    id_procedimento = request.form.get("id_procedimento")
    if not id_procedimento:
        return{"sucess":False, "message": "id_procedimento é obrigatório!"}, 400

    nova_data_procedimento = request.form.get("data_procedimento")
    novo_recebimento_paciente = request.form.get("recebimento")
    novo_despesa_hospitalar = request.form.get("despesa")
    novo_id_profissional = request.form.get("id_profissional")
    novo_id_especialidade = request.form.get("id_especialidade")
    novo_id_recebimento_paciente = request.form.get("id_recebimento_paciente")
    novo_id_despesa_hospitalar = request.form.get("id_despesa_hospitalar")
    novo_id_tipo_procedimento = request.form.get("id_tipo_procedimento")
    novo_id_equipamento = request.form.get("id_equipamento")

    try:
        query_procedimento = banco.session.query(procedimentos.Procedimento).where(procedimentos.Procedimento.id_procedimento==id_procedimento).first()

        if novo_recebimento_paciente:
            query_procedimento.id_recebimento_paciente = novo_recebimento_paciente
        if novo_despesa_hospitalar:
            query_procedimento.id_despesa_hospitalar = novo_despesa_hospitalar
        if nova_data_procedimento:
            nova_data_procedimento = datetime.strptime(nova_data_procedimento,"%d/%m/%Y %H:%M")
            query_procedimento.data_procedimento = nova_data_procedimento
        if novo_id_profissional:
            query_procedimento.id_profissional = novo_id_profissional
        if novo_id_especialidade:
            query_procedimento.id_especialidade = novo_id_especialidade
        if novo_id_recebimento_paciente:
            query_procedimento.id_recebimento_paciente = novo_recebimento_paciente
        if novo_id_despesa_hospitalar:
            query_procedimento.id_despesa_hospitalar = novo_id_despesa_hospitalar
        if novo_id_tipo_procedimento:
            query_procedimento.id_tipo_procedimento = novo_id_tipo_procedimento
        if novo_id_equipamento:
            query_procedimento.id_equipamento = novo_id_equipamento

        banco.session.commit()
        return{"sucess":True, "message": "Dados do procedimento atualizados com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao atualizar os dados do procedimento!"}, 400


# Deletar um procedimento existente
@procedimento.route('/deletar_procedimento', methods=['DELETE'])
def deletar_procedimento():
    id_procedimento = request.form.get("id_procedimento")
    query_procedimento = banco.session.query(procedimentos.Procedimento).where(procedimentos.Procedimento.id_procedimento==id_procedimento).first()
    try:
        banco.session.delete(query_procedimento)
        banco.session.commit()
        return{"sucess":True, "message": "Procedimento deletado com sucesso!"}, 201
    except Exception as err:
        print(err)
        return{"sucess":False, "message": "Falha ao deletar o procedimento!"}, 400






@tipo_procedimento.route('/criar_tipo_procedimento', methods=['POST'])
def criar_tipo_procedimento():
    nome_procedimento = request.form.get("nome_procedimento")
    categoria = request.form.get("categoria")
    custo_base_str = request.form.get("custo_base")
    risco = request.form.get("risco")
    equipamentos_necessarios = request.form.get("equipamentos_necessarios")

    # Verificação de campos obrigatórios
    if not nome_procedimento or not categoria or not custo_base_str or not risco or not equipamentos_necessarios:
        return {"success": False, "message": "Todos os campos são obrigatórios!"}, 400

    # Limpeza do valor custo_base (ex: "R$2.500,00" → "2500.00")
    try:
        # Remove "R$", pontos de milhar e troca vírgula por ponto
        valor_limpo = re.sub(r"[^\d,]", "", custo_base_str).replace(",", ".")
        custo_base = Decimal(valor_limpo)
    except (InvalidOperation, TypeError, ValueError):
        return {"success": False, "message": "O campo custo_base deve ser um número válido!"}, 400

    # Criação do objeto
    novo_tipo_procedimento = tipos_procedimentos.Tipo_Procedimento(
        nome_procedimento=nome_procedimento,
        categoria=categoria,
        custo_base=custo_base,
        risco=risco,
        equipamentos_necessarios=equipamentos_necessarios
    )

    # Tentativa de inserção no banco
    try:
        banco.session.add(novo_tipo_procedimento)
        banco.session.commit()
        return {"success": True, "message": "Tipo de procedimento cadastrado com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        print("Erro:", err)
        return {"success": False, "message": "Falha ao cadastrar o tipo de procedimento."}, 400






# Listar todos os tipos de procedimento
@tipo_procedimento.route("/listar_tipo_procedimento", methods=["GET"])
def listar_tipos_procedimentos():
    tipos_procedimentos_query = select(
        tipos_procedimentos.Tipo_Procedimento.nome_procedimento,
        tipos_procedimentos.Tipo_Procedimento.categoria,
        tipos_procedimentos.Tipo_Procedimento.custo_base,
        tipos_procedimentos.Tipo_Procedimento.risco,
        tipos_procedimentos.Tipo_Procedimento.equipamentos_necessarios
    )

    todos_tipos_procedimentos = banco.session.execute(tipos_procedimentos_query).all()

    lista = []
    for tipo_procedimento in todos_tipos_procedimentos:
        lista.append({
            "nome_procedimento": tipo_procedimento.nome_procedimento,
            "categoria": tipo_procedimento.categoria,
            "custo_base": str(tipo_procedimento.custo_base),  # mantém como string exata "1234.56"
            "risco": tipo_procedimento.risco,
            "equipamentos_necessarios": tipo_procedimento.equipamentos_necessarios
        })

    return jsonify({"success": True, "todos_tipos_procedimentos": lista})



# Obter detalhes de um tipo de procedimento por ID
@tipo_procedimento.route("/obter_tipo_procedimento", methods=["GET"])
def obter_tipo_procedimento():
    id_tipo_procedimento = request.form.get("id_tipo_procedimento")
    if not id_tipo_procedimento:
        return{"sucess":False, "message": "O id_tipo_procedimento é obrigatório!"}, 400
    try:
        todos_tipos_procedimentos = banco.session.query(tipos_procedimentos.Tipo_Procedimento).where(tipos_procedimentos.Tipo_Procedimento.id_tipo_procedimento == id_tipo_procedimento).all()
        lista = []
        for procedimento in todos_tipos_procedimentos:
            lista.append({
                "nome_procedimento":procedimento.nome_procedimento,
                "categoria":procedimento.categoria,
                "custo_base":procedimento.custo_base,
                "risco":procedimento.risco,
                "equipamentos_necessarios":procedimento.equipamentos_necessarios
            })
        return{"sucess":True, "todos_tipos_procedimentos": lista}
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Erro ao obter o tipo de procedimento!"}, 400