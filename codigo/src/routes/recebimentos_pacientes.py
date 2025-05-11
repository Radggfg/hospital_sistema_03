# Rotas para gerenciamento de recebimentos de pacientes
from flask import Blueprint, request
from src import banco
from src.db import paciente
from datetime import datetime
from sqlalchemy import select

# Cria blueprint para agrupamento das rotas de recebimento
recebimento_paciente = Blueprint('recebimento_paciente', __name__, url_prefix="/recebimento_paciente")

# Rota para criar um novo recebimento de paciente
@recebimento_paciente.route('/criar_recebimento', methods=['POST'])
def criar_recebimento():
    id_paciente = request.form.get("id_paciente")
    id_consulta = request.form.get("id_consulta")
    id_procedimento = request.form.get("id_procedimento")
    id_exame = request.form.get("id_exame")
    id_medicamento = request.form.get("id_medicamento")
    valor_total = request.form.get("valor_total")
    id_pagamento = request.form.get("id_pagamento")
    id_tipo_pagamento = request.form.get("id_tipo_pagamento")
    data_recebimento = request.form.get("data_recebimento")

    data_recebimento = datetime.strptime(data_recebimento, "%d/%m/%Y %H:%M:%S")

    # Verificação de obrigatoriedade dos campos
    if not id_paciente or not id_consulta or not id_procedimento or not id_exame or not id_medicamento or not valor_total or not id_pagamento or not id_tipo_pagamento or not data_recebimento:
        return {"sucess": False, "message": "Todos os campos são obrigatórios!"}, 400

    novo_recebimento = paciente.Recebimento_Paciente(
        id_paciente=id_paciente,
        id_consulta=id_consulta,
        id_procedimento=id_procedimento,
        id_exame=id_exame,
        id_medicamento=id_medicamento,
        valor_total=valor_total,
        id_pagamento=id_pagamento,
        id_tipo_pagamento=id_tipo_pagamento,
        data_recebimento=data_recebimento
    )

    try:
        banco.session.add(novo_recebimento)
        banco.session.commit()
        return {"sucess": True, "message": "Pagamento recebido com sucesso!"}, 201
    except Exception as err:
        print(err)
        return {"sucess": False, "message": "Falha ao receber o pagamento!"}, 400




# Rota para listar todos os recebimentos
@recebimento_paciente.route('/listar_recebimento', methods=['GET'])
def listar_recebimento():
    try:
        recebimentos_query = select(
            paciente.Recebimento_Paciente.id_recebimento_paciente,
            paciente.Recebimento_Paciente.id_paciente,
            paciente.Recebimento_Paciente.id_consulta,
            paciente.Recebimento_Paciente.id_procedimento,
            paciente.Recebimento_Paciente.id_exame,
            paciente.Recebimento_Paciente.id_medicamento,
            paciente.Recebimento_Paciente.valor_total,
            paciente.Recebimento_Paciente.id_pagamento,
            paciente.Recebimento_Paciente.id_tipo_pagamento,
            paciente.Recebimento_Paciente.data_recebimento
        )

        resultados = banco.session.execute(recebimentos_query).all()

        lista = []
        for recebimento in resultados:
            lista.append({
                "id_recebimento_paciente": recebimento.id_recebimento_paciente,
                "id_paciente": recebimento.id_paciente,
                "id_consulta": recebimento.id_consulta,
                "id_procedimento": recebimento.id_procedimento,
                "id_exame": recebimento.id_exame,
                "id_medicamento": recebimento.id_medicamento,
                "valor_total": float(recebimento.valor_total) if recebimento.valor_total else None,
                "id_pagamento": recebimento.id_pagamento,
                "id_tipo_pagamento": recebimento.id_tipo_pagamento,
                "data_recebimento": recebimento.data_recebimento.strftime("%d/%m/%Y %H:%M:%S") if recebimento.data_recebimento else None
            })

        return {"success": True, "todos_recebimentos_pacientes": lista}, 200

    except Exception as err:
        print(f"Erro ao listar recebimentos: {err}")
        banco.session.rollback()
        return {"success": False, "message": "Erro interno ao listar recebimentos!"}, 500



@recebimento_paciente.route('/buscar_recebimento', methods=['GET'])
def buscar_recebimento():
    id_recebimento_paciente = request.form.get("id_recebimento_paciente")
    if not id_recebimento_paciente:
        return {"success": False, "message": "O id do recebimento do paciente é obrigatório!"}, 400

    try:
        recebimento = banco.session.query(paciente.Recebimento_Paciente).filter_by(
            id_recebimento_paciente=id_recebimento_paciente
        ).first()

        if not recebimento:
            return {"success": False, "message": "Recebimento não encontrado!"}, 404

        retorno = {
            "id_recebimento_paciente": recebimento.id_recebimento_paciente,
            "id_paciente": recebimento.id_paciente,
            "id_consulta": recebimento.id_consulta,
            "id_procedimento": recebimento.id_procedimento,
            "id_exame": recebimento.id_exame,
            "id_medicamento": recebimento.id_medicamento,
            "valor_total": float(recebimento.valor_total) if recebimento.valor_total else None,
            "id_pagamento": recebimento.id_pagamento,
            "id_tipo_pagamento": recebimento.id_tipo_pagamento,
            "data_recebimento": recebimento.data_recebimento.strftime("%d/%m/%Y %H:%M:%S") if recebimento.data_recebimento else None
        }

        return {"success": True, "message": "Recebimento encontrado!", "recebimento": retorno}, 200

    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"success": False, "message": "Falha ao encontrar o recebimento!"}, 500





@recebimento_paciente.route('/atualizar_recebimento', methods=['PUT'])
def atualizar_recebimento():
    id_recebimento_paciente = request.form.get("id_recebimento_paciente")
    if not id_recebimento_paciente:
        return {"success": False, "message": "id_recebimento_paciente é obrigatório!"}, 400

    nova_data_recebimento = request.form.get("data_recebimento")
    novo_valor_total = request.form.get("valor_total")

    try:
        recebimento = banco.session.query(paciente.Recebimento_Paciente).filter_by(
            id_recebimento_paciente=id_recebimento_paciente
        ).first()

        if not recebimento:
            return {"success": False, "message": "Recebimento não encontrado!"}, 404

        if nova_data_recebimento:
            try:
                recebimento.data_recebimento = datetime.strptime(nova_data_recebimento, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return {"success": False, "message": "Formato de data inválido. Use dd/mm/yyyy HH:MM:SS."}, 400

        if novo_valor_total:
            try:
                recebimento.valor_total = float(novo_valor_total)
            except ValueError:
                return {"success": False, "message": "Valor total inválido."}, 400

        banco.session.commit()
        return {"success": True, "message": "Dados de recebimento atualizados com sucesso!"}, 200

    except Exception as err:
        print(f"Erro ao atualizar recebimento: {err}")
        banco.session.rollback()
        return {"success": False, "message": "Erro interno ao atualizar recebimento!"}, 500






# Rota para deletar um recebimento pelo ID
@recebimento_paciente.route('/deletar_recebimento', methods=['DELETE'])
def deletar_recebimento():
    id_recebimento_paciente = request.form.get("id_recebimento_paciente")
    query_recebimento = banco.session.query(paciente.Recebimento_Paciente).where(
        paciente.Recebimento_Paciente.id_recebimento_paciente == id_recebimento_paciente
    ).first()
    try:
        banco.session.delete(query_recebimento)
        banco.session.commit()
        return {"sucess": True, "message": "Recebimento deletado com sucesso!"}, 201
    except Exception as err:
        return {"sucess": False, "message": "Falha ao deletar o recebimento!"}, 400
