from flask import Blueprint, request
from src import banco
from src.db import especialidades, escalas_trabalhistas
from sqlalchemy import select
from datetime import datetime
from src.db.profissional import Profissional, Profissional_Leito
from sqlalchemy import and_



profissional = Blueprint("profissional", __name__, url_prefix="/profissional")
especialidade = Blueprint("especialidade",__name__,url_prefix = "/especialidade")
profissional_leito = Blueprint("profissional_leito",__name__,url_prefix = "/profissional_leito")

# Consulta dados de um profissional pelo CPF
@profissional.route("/consultar_profissional",methods = ["GET"])
def consultar_profissional():
    cpf = request.form.get("cpf")
    if not cpf:
        return{"sucess":False, "message": "O cpf do profissional é obrigatório!"}, 400
    try:
        query_profissional = banco.session.query(profissional.Profissional).where(profissional.Profissional.cpf==cpf).first()
        if not query_profissional:
            return{"sucess":False, "message": "O profissional não foi cadastrado!"}, 404
        resultado = {
        "nome":query_profissional.nome,
        "email":query_profissional.email,
        "id_especialidade":query_profissional.id_especialidade,
        "cargo":query_profissional.cargo,
        "cod_registro":query_profissional.cod_registro,
        "cpf":query_profissional.cpf,
        "carteira_trabalho":query_profissional.carteira_trabalho,
        "departamento":query_profissional.departamento,
        "data_nascimento":query_profissional.data_nascimento,
        "status":query_profissional.status
    }
        return{"sucess":True, "message": "O cpf do profissional foi encontrado!", "profissional":resultado}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao encontrar o cpf do profissional!"}, 400

# Lista todos os profissionais
@profissional.route("/listar_profissional",methods = ["GET"])
def listar_profissional():
    profissionais_query = select(profissional.Profissional.nome,
                                profissional.Profissional.email,
                                profissional.Profissional.id_especialidade,
                                profissional.Profissional.cargo,
                                profissional.Profissional.cod_registro,
                                profissional.Profissional.cpf,
                                profissional.Profissional.carteira_trabalho,
                                profissional.Profissional.departamento,
                                profissional.Profissional.data_nascimento,
                                profissional.Profissional.status)
    todos_profissionais = banco.session.execute(profissionais_query).all()
    lista = []
    for pessoa in todos_profissionais:
        lista.append({
            "nome":pessoa.nome,
            "email":pessoa.email,
            "id_especialidade":pessoa.id_especialidade,
            "cargo":pessoa.cargo,
            "cod_registro":pessoa.cod_registro,
            "cpf":pessoa.cpf,
            "carteira_trabalho":pessoa.carteira_trabalho,
            "departamento":pessoa.departamento,
            "data_nascimento":pessoa.data_nascimento,
            "status":pessoa.status
        })
    return{"sucess":True, "todos_profissionais":lista}

# Cadastra um novo profissional
@profissional.route("/cadastrar_profissional",methods = ["POST"])
def cadastrar_profissional():
    nome = request.form.get("nome")
    email = request.form.get("email")
    id_especialidade = request.form.get("id_especialidade")
    cargo = request.form.get("cargo")
    cod_registro = request.form.get("cod_registro")
    cpf = request.form.get("cpf")
    carteira_trabalho = request.form.get("carteira_trabalho")
    departamento = request.form.get("departamento")
    data_nascimento = request.form.get("data_nascimento")

    data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")

    if not nome or not id_especialidade or not cargo or not cod_registro or not cpf or not carteira_trabalho or not data_nascimento:
        return {"sucess":False, "message":"nome, id_especialidade, cargo, cod_registro, cpf, carteira_trabalho, data_nascimento são obrigatórios!"}, 400

    novo_profissional = profissional.Profissional(nome = nome,
                                                email = email, 
                                                id_especialidade = id_especialidade, 
                                                cargo = cargo, 
                                                cod_registro = cod_registro, 
                                                cpf = cpf, 
                                                carteira_trabalho = carteira_trabalho,
                                                departamento = departamento, 
                                                data_nascimento = data_nascimento,
                                                status = 'ativo')

    try:
        banco.session.add(novo_profissional)
        banco.session.commit()
        return{"sucess":True, "message": "Profissional cadastrado!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao inserir no banco de dados!"}, 400

# Atualiza dados do profissional
@profissional.route("/atualizar_profissional",methods = ["PUT"])
def atualizar_profissional():
    cpf_profissional = request.form.get("cpf")
    if not cpf_profissional:
        return {"sucess":False, "message":"cpf é obrigatório!"}, 400

    novo_cod_registro = request.form.get("cod_registro")
    novo_departamento = request.form.get("departamento")
    novo_cargo = request.form.get("cargo")
    nova_especialidade = request.form.get("especialidade")

    try:
        query_profissional = banco.session.query(profissional.Profissional).where(profissional.Profissional.cpf==cpf_profissional).first()
        if novo_cod_registro:
            query_profissional.cod_registro = novo_cod_registro
        if novo_departamento:
            query_profissional.departamento = novo_departamento
        if novo_cargo:
            query_profissional.cargo = novo_cargo
        if nova_especialidade:
            query_profissional.id_especialidade = nova_especialidade
        banco.session.commit()
        return{"sucess":True, "message": "Profissional atualizado com sucesso!"}
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao atualizar o registro do profissional no banco de dados!"}, 400


#  Listar todas as especialidades cadastradas no sistema
@especialidade.route("/listar_especialidade", methods=["GET"])
def listar_especialidades():
    # Consulta todas as especialidades no banco de dados e retorna em uma lista
    especialidades_query = select(especialidades.Especialidade.nome_especialidade)
    todas_especialidades = banco.session.execute(especialidades_query).all()
    lista = []
    for especialidade in todas_especialidades:
        lista.append(especialidade.nome_especialidade)
    return{"sucess":True, "todas_especialidades":lista}

# Buscar profissionais por especialidade
@especialidade.route("/buscar_especialidade", methods=["GET"])
def buscar_por_especialidade():
    # Retorna os nomes das especialidades relacionadas ao id fornecido
    id_especialidade = request.form.get("id_especialidade")
    if not id_especialidade:
        return{"sucess":False, "message": "O id da especialidade é obrigatório!"}, 400
    try:
        query_especialidade = banco.session.query(especialidades.Especialidade).where(especialidades.Especialidade.id_especialidade==id_especialidade).all()
        if not query_especialidade:
            return{"sucess":False, "message": "Nenhuma especialidade encontrada!"}, 400
        lista = []
        for especialidade in query_especialidade:
            lista.append(especialidade.nome_especialidade)
            return{"sucess":True, "message": "Lista de especialidades encontrada com sucesso!", "especialidade":lista}, 201
    except Exception as err:
        return{"sucess":False, "message": "Falha ao encontrar a lista de especialidades!"}, 400

# Criar nova especialidade
@especialidade.route('/criar_especialidade', methods=['POST'])
def criar_especialidade():
    # Cadastra uma nova especialidade com o nome fornecido
    nome_especialidade = request.form.get("nome_especialidade")

    if not nome_especialidade:
        return{"sucess":False, "message": "nome_especialidade são obrigatórios!"}, 400
    nova_especialidade = especialidades.Especialidade(nome_especialidade = nome_especialidade)
    try:
        banco.session.add(nova_especialidade)
        banco.session.commit()
        return{"sucess":True, "message": "Especialidade cadastrada com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao cadastrar a especialidade!"}, 400

# Deletar especialidade
@especialidade.route('/deletar_especialidade', methods=['DELETE'])
def deletar_especialidade():
    # Remove uma especialidade com base no id fornecido
    id_especialidade = request.form.get("id_especialidade")
    query_especialidade = banco.session.query(especialidades.Especialidade).where(especialidades.Especialidade.id_especialidade==id_especialidade).first()
    try:
        banco.session.delete(query_especialidade)
        banco.session.commit()
        return{"sucess":True, "message": "Especialidade deletada com sucesso!"}, 201
    except Exception as err:
        print(err)
        return{"sucess":False, "message": "Falha ao deletar a especialidade!"}, 400

# Verificar a disponibilidade de um profissional
@profissional.route("/verificar_disponibilidade", methods=["GET"])
def verificar_disponibilidade():
    # Verifica se um profissional está disponível em uma data específica (simulado)
    id_profissional = request.form.get("cpf")
    data_movimentacao = request.form.get("data_movimentacao")
    horario = request.form.get("horario")


    if not id_profissional or not horario or not data_movimentacao:
        return {
            "success": False,
            "message": "O id do profissional, data de movimentação e horário são obrigatórios!"
        }, 400

    try:
        data_verificada = datetime.strptime(data_movimentacao, "%d/%m/%Y")



        disponibilidade = banco.session.query(
            escalas_trabalhistas.Escala_Trabalhista).where(escalas_trabalhistas.Escala_Trabalhista.id_profissional==id_profissional).filter(
                escalas_trabalhistas.Escala_Trabalhista.periodo_inicio < horario,
                escalas_trabalhistas.Escala_Trabalhista.periodo_fim > horario
            ).filter(
                escalas_trabalhistas.Escala_Trabalhista.data_escala_inicio < data_verificada,
                escalas_trabalhistas.Escala_Trabalhista.data_escala_fim > data_verificada
            )
        disponibilidade = disponibilidade.first()
        if not disponibilidade:
            return {
                "success": False,
                "message": "Profissional não encontrado ou não ossui escala!"
            }, 404
        return {
            "success": True,
            "message": f"Profissional está disponível na data {data_verificada.strftime('%H:%M:%S')} e no horário {horario}."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao verificar disponibilidade: {str(e)}"
        }, 500




# Consultar horário de trabalho de um profissional
@profissional.route("/consultar_horario_trabalho", methods=["GET"])
def consultar_horario_trabalho():
    escala_query = select(
        escalas_trabalhistas.Escala_Trabalhista.id_profissional,
        escalas_trabalhistas.Escala_Trabalhista.periodo_inicio,
        escalas_trabalhistas.Escala_Trabalhista.periodo_fim,
        escalas_trabalhistas.Escala_Trabalhista.id_escala,
        escalas_trabalhistas.Escala_Trabalhista.data_escala_inicio,
        escalas_trabalhistas.Escala_Trabalhista.data_escala_fim
    )
    todas_escalas = banco.session.execute(escala_query).all()
    lista = []
    for escala in todas_escalas:
        periodo_inicio = f"{escala.periodo_inicio.hour}:{escala.periodo_inicio.minute:02}"
        periodo_fim = f"{escala.periodo_fim.hour}:{escala.periodo_fim.minute:02}"
        data_escala_inicio = f"{escala.data_escala_inicio.day:02}/{escala.data_escala_inicio.month:02}/{escala.data_escala_inicio.year:04}"
        data_escala_fim = f"{escala.data_escala_fim.day:02}/{escala.data_escala_fim.month:02}/{escala.data_escala_fim.year:04}"
        lista.append({
            "id_profissional":escala.id_profissional,
            "periodo_inicio":periodo_inicio,
            "periodo_fim":periodo_fim,
            "id_escala":escala.id_escala,
            "data_escala_inicio":data_escala_inicio,
            "data_escala_fim":data_escala_fim
        })
    return{"sucess":True, "todas_escalas":lista}



# Atualizar status de um profissional (ativo, afastado, licença, etc)
@profissional.route("/atualizar_status", methods=["PUT"])
def atualizar_status():
    cpf = request.form.get("cpf")
    novo_status = request.form.get("status")

    if not cpf or not novo_status:
        return {
            "success": False,
            "message": "CPF e novo status são obrigatórios!"
        }, 400

    try:
        profissional_encontrado = banco.session.query(Profissional).filter_by(cpf=cpf).first()

        if not profissional_encontrado:
            return {
                "success": False,
                "message": "Profissional não encontrado!"
            }, 404

        profissional_encontrado.status = novo_status.lower().strip()
        banco.session.commit()

        return {
            "success": True,
            "message": f"Status do profissional atualizado para '{novo_status}'."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao atualizar status: {str(e)}"
        }, 500

# Criar associação entre profissional e leito
@profissional_leito.route("/criar_profissional_leito", methods=["POST"])
def criar_profissional_leito():
    id_profissional = request.form.get("id_profissional")
    id_leito = request.form.get("id_leito")
    data_atribuicao = request.form.get("data_atribuicao")
    turno = request.form.get("turno")
    status = request.form.get("status")

    data_atribuicao = datetime.strptime(data_atribuicao, "%d/%m/%Y")

    if not id_profissional or not id_leito or not data_atribuicao or not turno or not status:
        return{"sucess":False, "message": "id_profissional, id_leito, data_atribuicao, turno e status são obrigatórios!"}, 400

    # OBS: A lógica abaixo está incorreta, está instanciando Profissional em vez da tabela de associação Profissional_Leito
    novo_profissional_leito = Profissional_Leito(id_profissional = id_profissional,
                                                            id_leito = id_leito,
                                                            data_atribuicao = data_atribuicao,
                                                            turno = turno,
                                                            status = status)

    try:
        banco.session.add(novo_profissional_leito)
        banco.session.commit()
        return{"sucess":True, "message": "profissional_leito cadastrado!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao cadastrar o profissional_leito!"}, 400

# As próximas rotas de CRUD para profissional_leito estão como placeholders e devem ser implementadas
@profissional_leito.route("/listar_profissional_leito", methods=["GET"])
def listar_profissional_leito():
    profissionais_query = select(
        Profissional_Leito.id_profissional_leito,
        Profissional_Leito.id_profissional,
        Profissional_Leito.id_leito,
        Profissional_Leito.data_atribuicao,
        Profissional_Leito.turno,
        Profissional_Leito.status,
    )

    todos_profissionais_leitos = banco.session.execute(profissionais_query).all()

    lista = []
    for prof in todos_profissionais_leitos:
        lista.append({
            "id_leito":prof.id_leito,
            "id_profissional_leito":prof.id_profissional_leito,
            "id_profissional":prof.id_profissional,
            "data_atribuicao":prof.data_atribuicao,
            "turno":prof.turno,
            "status":prof.status
        })
    return{"sucess":True, "todos_profissionais_leitos":lista}

@profissional_leito.route("/obter_profissional_leito", methods=["GET"])
def obter_profissional_leito():
    id_profissional_leito = request.form.get("id_profissional_leito")
    if not id_profissional_leito:
        return{"sucess":False, "message": "id_profissional_leito é obrigatório!"}, 400

    query_obter_profissional_leito = banco.session.query(Profissional_Leito).where(Profissional_Leito.id_profissional_leito==id_profissional_leito).first()
    if not query_obter_profissional_leito:
        return{"sucess":False, "message": "id_profissional_leito nã oexiste!"}, 400

    return{"sucess":True, "message": "id_paciente_leito foi encontrado!",
        "id_profissional": query_obter_profissional_leito.id_profissional,
        "id_leito": query_obter_profissional_leito.id_leito,
        "data_atribuicao": query_obter_profissional_leito.data_atribuicao,
        "turno": query_obter_profissional_leito.turno,
        "status": query_obter_profissional_leito.status,
        "observacoes": query_obter_profissional_leito.observacoes}, 201

@profissional_leito.route("/atualizar_profissional_leito", methods=["PUT"])
def atualizar_profissional_leito():
    id_profissional_leito = request.form.get("id_profissional_leito")
    if not id_profissional_leito:
        return{"sucess":False, "message": "id_profissional_leito é obrigatório!"}, 400

    novo_profissional_leito = request.form.get("id_profissional_leito")
    nova_data_atribuicao = request.form.get("data_atribuicao")
    novo_turno = request.form.get("turno")
    novo_status = request.form.get("status")

    nova_data_atribuicao = datetime.strptime(nova_data_atribuicao, "%d/%m/%Y")

    try:
        query_profissional_leito = banco.session.query(Profissional_Leito).where(Profissional_Leito.id_profissional_leito==id_profissional_leito).first()
        if novo_profissional_leito:
            query_profissional_leito.id_profissional_leito = novo_profissional_leito
        if nova_data_atribuicao:
            query_profissional_leito.data_atribuicao = nova_data_atribuicao
        if novo_turno:
            query_profissional_leito.turno = novo_turno
        if novo_status:
            query_profissional_leito.status = novo_status
            banco.session.commit()
            return{"sucess":True, "message": "Dados do profissional_leito atualizados com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao atualizar os dados do profissional_leito!"}, 400


@profissional_leito.route("/deletar_profissional_leito", methods=["DELETE"])
def deletar_profissional_leito():
    id_profissional_leito = request.form.get("id_profissional_leito")
    query_profissional_leito = banco.session.query(Profissional_Leito).where(Profissional_Leito.id_profissional_leito==id_profissional_leito).first()
    try:
        banco.session.delete(query_profissional_leito)
        banco.session.commit()
        return{"sucess":True, "message": "Profissional_leito deletado com sucesso!"}, 201
    except Exception as err:
        print(err)
        return{"sucess":False, "message": "Falha ao deletar o Profissional_leito!"}, 400

