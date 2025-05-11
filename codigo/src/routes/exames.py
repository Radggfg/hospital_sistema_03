from flask import Blueprint, request
from src import banco
from src.db import paciente, consultas, profissional, prontuarios, exames
from datetime import datetime
from sqlalchemy import select, Column, Enum



exame = Blueprint("exame",__name__,url_prefix = "/exame")

# Rota para cadastrar um novo exame
@exame.route("/cadastrar_exame",methods = ["POST"])
def cadastrar_exame():
    tipo_exame = request.form.get("tipo_exame")
    descricao_exame = request.form.get("descricao_exame")
    data_solicitacao = request.form.get("data_solicitacao")
    status_exame = request.form.get("status_exame")
    resultado_exame = request.form.get("resultado_exame")
    assinatura_profissional = request.form.get("assinatura_profissional")
    id_procedimento = request.form.get("id_procedimento")
    id_prontuario = request.form.get("id_prontuario")
    id_paciente = request.form.get("id_paciente")
    id_profissional = request.form.get("id_profissional")

    data_solicitacao = datetime.strptime(data_solicitacao, "%d/%m/%Y %H:%M:%S")

    if not tipo_exame or not descricao_exame or not data_solicitacao or not status_exame or not resultado_exame or not assinatura_profissional or not id_procedimento or not id_prontuario or not id_paciente or not id_profissional:
        return{"sucess":False, "message": "Todos os campos são obrigatórios!"}, 400

    novo_exame = exames.Exame(
        tipo_exame = tipo_exame,
        descricao_exame = descricao_exame,
        data_solicitacao = data_solicitacao,
        status_exame = status_exame,
        resultado_exame = resultado_exame,
        assinatura_profissional = assinatura_profissional,
        id_procedimento = id_procedimento,
        id_prontuario = id_prontuario,
        id_paciente = id_paciente,
        id_profissional = id_profissional)
    try:
        banco.session.add(novo_exame)
        banco.session.commit()
        return {"success": True, "message": "Exame cadastrado com sucesso."}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"success": False, "message": "Erro ao cadastrar o exame!"}, 400




# Rota para remarcar exame
@exame.route("/remarcar_exame", methods=["PUT"])
def remarcar_exame():
    # Obtém o ID do exame
    id_exame = request.form.get("id_exame")
    if not id_exame:
        return {"success": False, "message": "O id_exame é obrigatório!"}, 400

    # Obtém as novas datas do formulário
    nova_data_solicitada = request.form.get("data_solicitada")
    nova_data_realizacao = request.form.get("data_realizacao")

    try:
        # Busca o exame no banco
        exame_encontrado = banco.session.query(exames.Exame).filter_by(id_exame=id_exame).first()

        if not exame_encontrado:
            return {"success": False, "message": "Exame não encontrado!"}, 404

        # Converte e valida a nova data de solicitação, se fornecida
        if nova_data_solicitada:
            try:
                exame_encontrado.data_solicitacao = datetime.strptime(nova_data_solicitada, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return {
                    "success": False,
                    "message": "Formato inválido para data_solicitada. Use: DD/MM/AAAA HH:MM:SS"
                }, 400

        # Converte e valida a nova data de realização, se fornecida
        if nova_data_realizacao:
            try:
                exame_encontrado.data_realizacao = datetime.strptime(nova_data_realizacao, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return {
                    "success": False,
                    "message": "Formato inválido para data_realizacao. Use: DD/MM/AAAA HH:MM:SS"
                }, 400

        # Confirma as alterações no banco
        banco.session.commit()

        return {"success": True, "message": "Exame remarcado com sucesso!"}, 200

    except Exception as err:
        banco.session.rollback()
        return {
            "success": False,
            "message": f"Erro ao remarcar exame: {str(err)}"
        }, 500







# Rota para cancelar exame
@exame.route("/cancelar_exame", methods=["PUT"])
def cancelar_exame():
    id_exame = request.form.get("id_exame")

    if not id_exame:
        return {"success": False, "message": "id_exame é obrigatório!"}, 400

    try:
        exame_cadastro = banco.session.query(exames.Exame).where(exames.Exame.id_exame == id_exame).first()

        if not exame_cadastro:
            return {"success": False, "message": "Exame não encontrado!"}, 404

        exame_cadastro.status_exame = exames.Exame.StatusExameEnum.cancelado  # Enum corretamente usado
        banco.session.commit()

        return {"success": True, "message": "Exame cancelado com sucesso!"}

    except Exception as err:
        banco.session.rollback()
        return {"success": False, "message": f"Erro ao cancelar exame: {str(err)}"}, 400


# Rota que lista todos os exames
@exame.route("/listar_exame", methods=["GET"])
def listar_exame():
    # Monta a query de seleção dos campos desejados
    exame_query = select(
        exames.Exame.tipo_exame,
        exames.Exame.descricao_exame,
        exames.Exame.data_solicitacao,
        exames.Exame.data_realizacao,
        exames.Exame.status_exame,
        exames.Exame.resultado_exame,
        exames.Exame.assinatura_profissional,
        exames.Exame.id_exame,
        exames.Exame.id_procedimento,
        exames.Exame.id_prontuario,
        exames.Exame.id_paciente,
        exames.Exame.id_profissional
    )

    # Executa a query
    todos_exames = banco.session.execute(exame_query).all()

    lista = []
    for row in todos_exames:
        data_solicitacao = row.data_solicitacao.strftime("%d/%m/%Y %H:%M:%S") if row.data_solicitacao else None
        data_realizacao = row.data_realizacao.strftime("%d/%m/%Y %H:%M:%S") if row.data_realizacao else None

        lista.append({
            "tipo_exame": row.tipo_exame,
            "descricao_exame": row.descricao_exame,
            "data_solicitacao": data_solicitacao,
            "data_realizacao": data_realizacao,
            "status_exame": row.status_exame.value if row.status_exame else None,
            "resultado_exame": row.resultado_exame.value if row.resultado_exame else None,
            "assinatura_profissional": row.assinatura_profissional,
            "id_exame": row.id_exame,
            "id_procedimento": row.id_procedimento,
            "id_prontuario": row.id_prontuario,
            "id_paciente": row.id_paciente,
            "id_profissional": row.id_profissional,
        })

    return {
        "success": True,
        "quantidade": len(lista),
        "dados": lista
    }




# Deletar exame
@exame.route("/deletar_exame",methods = ["DELETE"])
def deletar_exame():
    id_exame = request.form.get("id_exame")
    if not id_exame:
        return{"sucess":False, "message": "id_exame é obrigatório!"}, 400
    try:
        cadastro_exame = banco.session.query(exames.Exame).filter_by(id_exame=id_exame).first()
        if not cadastro_exame:
            return{"sucess":False, "message": "Exame não encontrado!"}, 400
    
        banco.session.delete(cadastro_exame)
        banco.session.commit()
        return{"sucess":True, "message": "Exame deletado com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao deletar o exame!"}, 400





# Rota para obter o status de um exame
@exame.route("/status_exame", methods=["GET"])
def status_exame():
    id_exame = request.form.get("id_exame")
    if not id_exame:
        return{"sucess": False, "message": "O id_exame é obrigatório!"}, 400
    try:
        query_exame = banco.session.query(exames.Exame).where(exames.Exame.id_exame==id_exame).first()
        if not query_exame:
            return{"sucess": False, "message": "O id_exame não foi encontrado!"}, 400

        status = {
            "tipo_exame": query_exame.tipo_exame,
            "descricao_exame": query_exame.descricao_exame,
            "data_solicitacao": query_exame.data_solicitacao,
            "data_realizacao": query_exame.data_realizacao,
            "status_exame": query_exame.status_exame,
            "resultado_exame": query_exame.resultado_exame,
            "id_exame": query_exame.id_exame,
            "id_profissional": query_exame.id_profissional,
            "id_paciente": query_exame.id_paciente}
        return{"sucess":True, "message": "O exame foi encontrado!", "exame":status}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Erro ao encontrar o exame!"}, 400




# Rota para alterar status e dados de um exame
@exame.route("/alterar_status", methods=["PUT"])
def alterar_status_exame():
    id_exame = request.form.get("id_exame")

    if not id_exame:
        return {"success": False, "message": "O id_exame é obrigatório!"}, 400

    nova_descricao_exame = request.form.get("descricao_exame")
    nova_data_solicitacao = request.form.get("data_solicitacao")
    nova_data_realizacao = request.form.get("data_realizacao")
    novo_status_exame = request.form.get("status_exame")
    novo_resultado_exame = request.form.get("resultado_exame")
    novo_profissional = request.form.get("id_profissional")
    nova_assinatura_profissional = request.form.get("assinatura_profissional")
    novo_laudo_medico = request.form.get("laudo_medico")

    try:
        query_exame = banco.session.query(exames.Exame).where(exames.Exame.id_exame == id_exame).first()

        if not query_exame:
            return {"success": False, "message": "Exame não encontrado!"}, 404

        if nova_descricao_exame:
            query_exame.descricao_exame = nova_descricao_exame

        if nova_data_solicitacao:
            try:
                query_exame.data_solicitacao = datetime.strptime(nova_data_solicitacao, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return {"success": False, "message": "Formato inválido para data_solicitacao"}, 400

        if nova_data_realizacao:
            try:
                query_exame.data_realizacao = datetime.strptime(nova_data_realizacao, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                return {"success": False, "message": "Formato inválido para data_realizacao"}, 400

        if novo_status_exame:
            try:
                query_exame.status_exame = exames.Exame.StatusExameEnum(novo_status_exame)
            except ValueError:
                return {"success": False, "message": f"Status '{novo_status_exame}' inválido!"}, 400

        if novo_resultado_exame:
            try:
                query_exame.resultado_exame = exames.Exame.ResultadoExameEnum(novo_resultado_exame)
            except ValueError:
                return {"success": False, "message": f"Resultado '{novo_resultado_exame}' inválido!"}, 400

        if novo_profissional:
            query_exame.id_profissional = novo_profissional

        if nova_assinatura_profissional:
            query_exame.assinatura_profissional = nova_assinatura_profissional

        if novo_laudo_medico:
            query_exame.laudo_medico = novo_laudo_medico

        banco.session.commit()
        return {"success": True, "message": "Dados do exame atualizados com sucesso!"}, 200

    except Exception as err:
        banco.session.rollback()
        print("Erro:", err)
        return {"success": False, "message": "Falha ao atualizar os dados do exame!"}, 500





# Consultar laudo médico de um exame
@exame.route("/consultar_laudo", methods=["GET"])
def consultar_laudo():
    id_exame = request.args.get("id_exame")  

    if not id_exame:
        return {"success": False, "message": "id_exame é obrigatório!"}, 400

    try:
        id_exame = int(id_exame)  # Garante que é um número
    except ValueError:
        return {"success": False, "message": "id_exame deve ser um número inteiro!"}, 400

    try:
        query_exame = banco.session.query(exames.Exame).filter_by(id_exame=id_exame).first()

        if not query_exame:
            return {"success": False, "message": "Exame não encontrado!"}, 404

        return {
            "success": True,
            "message": "Laudo encontrado com sucesso!",
            "laudo_medico": query_exame.laudo_medico
        }, 200

    except Exception as err:
        banco.session.rollback()
        return {
            "success": False,
            "message": f"Erro ao buscar laudo: {str(err)}"
        }, 500




# Emitir laudo
@exame.route("/emitir_laudo", methods=["PUT"])
def emitir_laudo():
    id_exame = request.form.get("id_exame")
    emitir_laudo_novo = request.form.get("laudo_medico")
    if not id_exame:
        return{"sucess":False, "message": "id_exame é obrigatório!"}, 400
    try:
        query_laudo = banco.session.query(exames.Exame).where(exames.Exame.id_exame==id_exame).first()
        query_laudo.laudo_medico = emitir_laudo_novo
        banco.session.commit()
        return{"sucess":True, "message": "Laudo emitido!", "laudo_medico": query_laudo.laudo_medico}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Erro ao emitir laudo!"}, 400

# Buscar exames por paciente
@exame.route("/buscar_por_paciente", methods=["GET"])
def buscar_por_paciente():
    id_paciente = request.form.get("cpf")
    try:
        query_exame = banco.session.query(exames.Exame).where(exames.Exame.id_paciente==id_paciente).all()
        if not query_exame:
            return{"sucess":False, "message": "Nenhum exame encontrado!"}, 400
        return{"sucess":True, "message": "Exames encontrados!", "exames": [e.serialize() for e in query_exame]}, 201
    except Exception as err:
        return{"sucess":False, "message": "Erro ao buscar exames!"}, 400





# Buscar exames por profissional (a completar)
@exame.route("/buscar_por_profissional", methods=["GET"])
def buscar_por_profissional():
    cpf = request.form.get("cpf")
    if not cpf:
        return{"sucess":False, "message": "CPF é obrigatório!"}, 400
    return{"sucess":False, "message": "Funcionalidade não implementada."}, 501





# Histórico de exames de um paciente
@exame.route("/historico_exame", methods=["GET"])
def historico_exames():
    cpf = request.form.get("cpf")
    try:
        query_historico = banco.session.query(exames.Exame).where(exames.Exame.id_paciente==cpf).all()
        if not query_historico:
            return{"sucess":False, "message": "Nenhum histórico encontrado!"}, 400
        return{"sucess":True, "message": "Histórico encontrado!", "historico": [h.serialize() for h in query_historico]}, 201
    except Exception as err:
        return{"sucess":False, "message": "Erro ao buscar histórico!"}, 400
