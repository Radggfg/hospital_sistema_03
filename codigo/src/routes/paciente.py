# Rotas relacionadas ao módulo de pacientes e prontuários
from flask import Blueprint
from flask import request
from src import banco
from src.db import consultas, profissional, procedimentos, medicamentos, exames
from src.db. prontuarios import Prontuario 
from src.db import paciente as paciente_db
from datetime import datetime
from sqlalchemy import select

# Blueprints
pacientes = Blueprint("paciente",__name__,url_prefix = "/paciente")
prontuarios = Blueprint("prontuarios",__name__,url_prefix = "/prontuarios")
medicamentos = Blueprint("medicamentos",__name__,url_prefix = "/medicamentos")

# Consulta paciente por CPF
@pacientes.route("/consultar_paciente",methods = ["GET"])
def consultar_paciente():
    cpf = request.form.get("cpf")
    if not cpf:
        return{"sucess":False, "message": "O cpf do paciente é obrigatório!"}, 400
    try:
        query_paciente = banco.session.query(paciente_db.Paciente).where(paciente_db.Paciente.cpf==cpf).first()
        if not query_paciente:
            return{"sucess":False, "message": "O paciente não está cadastrado!"}, 404
        resultado = {
            "cpf":query_paciente.cpf,
            "data_nascimento":query_paciente.data_nascimento,
            "email":query_paciente.email,
            "endereco":query_paciente.endereco,
            "estado_civil":query_paciente.estado_civil,
            "nome":query_paciente.nome,
            "nome_convenio":query_paciente.nome_convenio,
            "num_convenio":query_paciente.num_convenio,
            "profissao":query_paciente.profissao,
            "responsavel":query_paciente.responsavel,
            "telefone":query_paciente.telefone,
            "telefone_contato":query_paciente.telefone_contato,
        }
        return{"sucess":True, "message": "O cpf do paciente_db foi encontrado!", "paciente_db":resultado}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao encontrar o cpf do paciente!"}, 400


# Criação de uma nova consulta
@pacientes.route("/criar_consulta",methods = ["POST"])
def criar_consulta():
    id_consulta = request.form.get("id_consulta")
    id_paciente = request.form.get("id_paciente")
    id_profissional = request.form.get("id_profissional")
    data_hora = request.form.get("data_hora")
    id_diagnostico = request.form.get("id_diagnostico")
    prescricao = request.form.get("prescricao")
    tipo_consulta = request.form.get("tipo_consulta")
    id_prontuario = request.form.get("id_prontuario")
    id_exame = request.form.get("id_exame")
    id_faturamento_hospitalar = request.form.get("id_faturamento_hospitalar")

    if not id_consulta or not id_paciente or not id_profissional or not data_hora or not tipo_consulta:
        return {"sucess":False, "message":"id_consulta, id_paciente, id_profissional, data_hora, tipo_consulta, são obrigatórios!"}, 400

    nova_consulta = consultas.Consulta(
        id_consulta = id_consulta, 
        id_paciente = id_paciente, 
        id_profissional = id_profissional,
        data_hora = data_hora,
        id_diagnostico = id_diagnostico,
        prescricao = prescricao,
        tipo_consulta = tipo_consulta,
        id_prontuario = id_prontuario,
        id_exame = id_exame,
        id_faturamento_hospitalar = id_faturamento_hospitalar
    )

    try:
        banco.session.add(nova_consulta)
        banco.session.commit()
        return{"sucess":True, "message": "Consulta agendada com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao inserir a consulta no banco de dados!"}, 400


# Cadastro de novo paciente
@pacientes.route("/cadastrar_paciente", methods = ["POST"])
def cadastrar_paciente():
    cpf = request.form.get("cpf")
    nome = request.form.get("nome")
    nome_convenio = request.form.get("nome_convenio")
    num_convenio = request.form.get("num_convenio")
    telefone = request.form.get("telefone")
    telefone_contato = request.form.get("telefone_contato")
    endereco = request.form.get("endereco")
    email = request.form.get("email")
    data_nascimento = request.form.get("data_nascimento")
    profissao = request.form.get("profissao")
    estado_civil = request.form.get("estado_civil")
    responsavel = request.form.get("responsavel")

    data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")

    if not cpf or not nome or not data_nascimento:
        return {"sucess":False, "message":"cpf, nome e data_nascimento são obrigatórios!"}, 400

    novo_paciente = paciente_db.Paciente(
        cpf = cpf, 
        nome = nome, 
        nome_convenio = nome_convenio,
        num_convenio = num_convenio,
        telefone = telefone,
        telefone_contato = telefone_contato,
        endereco = endereco,
        email = email,
        data_nascimento = data_nascimento,
        profissao = profissao,
        estado_civil = estado_civil,
        responsavel = responsavel
    )
    try:
        banco.session.add(novo_paciente)
        banco.session.commit()
        return{"sucess":True, "message": "Paciente cadastrado!"}, 201
    except Exception as err:
        banco.session.rollback()
        print(err)
        return{"sucess":False, "message": "Falha ao inserir no banco de dados!"}, 400


# Listagem de todos os pacientes
@pacientes.route("/listar_paciente", methods = ["GET"])
def listar_paciente():
    pacientes_query = select(
        paciente_db.Paciente.cpf, 
        paciente_db.Paciente.data_nascimento, 
        paciente_db.Paciente.email, 
        paciente_db.Paciente.endereco, 
        paciente_db.Paciente.estado_civil, 
        paciente_db.Paciente.nome, 
        paciente_db.Paciente.nome_convenio, 
        paciente_db.Paciente.num_convenio, 
        paciente_db.Paciente.profissao, 
        paciente_db.Paciente.responsavel, 
        paciente_db.Paciente.telefone, 
        paciente_db.Paciente.telefone_contato
    )
    todos_pacientes = banco.session.execute(pacientes_query).all() 
    lista = []
    for paciente in todos_pacientes:
        lista.append({
            "cpf":paciente.cpf,
            "data_nascimento":paciente.data_nascimento,
            "email":paciente.email,
            "endereco":paciente.endereco,
            "estado_civil":paciente.estado_civil,
            "nome":paciente.nome,
            "nome_convenio":paciente.nome_convenio,
            "num_convenio":paciente.num_convenio,
            "profissao":paciente.profissao,
            "responsavel":paciente.responsavel,
            "telefone":paciente.telefone,
            "telefone_contato":paciente.telefone_contato,
        })
    return{"sucess":True, "todos_paciente":lista}



# Atualização de dados de paciente
@pacientes.route("/atualizar_paciente", methods = ["PUT"])
def atualizar_paciente():
    cpf_paciente = request.form.get("cpf")
    if not cpf_paciente:
        return {"sucess":False, "message":"cpf é obrigatório!"}, 400

    novo_telefone = request.form.get("telefone")
    novo_telefone_contato = request.form.get("telefone_contato")
    novo_profissao = request.form.get("profissao")
    estado_civil = request.form.get("estado_civil")
    novo_email = request.form.get("email")
    novo_endereco = request.form.get("endereco") 

    try:
        query_paciente = banco.session.query(paciente_db.Paciente).where(paciente_db.Paciente.cpf==cpf_paciente).first()
        if novo_telefone:
            query_paciente.telefone = novo_telefone
        if novo_telefone_contato:
            query_paciente.telefone_contato = novo_telefone_contato
        if novo_profissao:
            query_paciente.profissao = novo_profissao
        if estado_civil:
            query_paciente.estado_civil = estado_civil
        if novo_email:
            query_paciente.email = novo_email
        if novo_endereco:
            query_paciente.endereco = novo_endereco

        banco.session.commit()
        return{"sucess":True, "message": "Dados do paciente atualizados com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return{"sucess":False, "message": "CPF não cadastrado no banco de dados!"}, 400

# Criação de prontuário
@prontuarios.route("/criar_prontuario", methods=["POST"])
def criar_prontuario():
    id_paciente = request.form.get("id_paciente")
    medico_responsavel = request.form.get("medico_responsavel")
    data_entrada = request.form.get("data_entrada")
    descricao = request.form.get("descricao")

    data_entrada = datetime.strptime(data_entrada, "%d/%m/%Y %H:%M:%S")

    novo_prontuario = Prontuario(id_paciente=id_paciente, 
                                            medico_responsavel=medico_responsavel, 
                                            data_entrada=data_entrada, 
                                            descricao=descricao)

    try:
        banco.session.add(novo_prontuario)
        banco.session.commit()
        return{"sucess":True, "message": "Consulta agendada com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao inserir o prontuario no banco de dados!"}, 400



# Atualização de prontuário
@prontuarios.route("/atualizar_prontuario", methods=["PUT"])
def atualizar_prontuario():
    id_prontuario = request.form.get("id_prontuario")
    if not id_prontuario:
        return{"sucess":False, "message": "id_prontuário é obrigatório!"}, 400

    novo_medico_responsavel = request.form.get("medico_responsavel")
    nova_descricao = request.form.get("descricao")

    try:
        query_prontuario = banco.session.query(Prontuario).where(Prontuario.id_prontuario==id_prontuario).first()
        nova_descricao = query_prontuario.descricao + "\n---\n" + nova_descricao
        if novo_medico_responsavel:
            query_prontuario.medico_responsavel = novo_medico_responsavel
        if nova_descricao:
            query_prontuario.descricao = nova_descricao

        banco.session.commit()
        return{"sucess":True, "message": "Dados do prontuário atualizados com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao atualizar os dados do prontuários!"}, 400





# Histórico médico do paciente
@pacientes.route("/historico_medico", methods=["GET"])
def historico_medico():
    cpf = request.form.get("cpf")
    if not cpf:
        return{"sucess":False, "message": "CPF é obrigatório!"}, 400
    historico_completo = {}
    try:
        query_historico = banco.session.query(procedimentos.Procedimento).where(procedimentos.Procedimento.id_paciente==cpf).all()
        if query_historico:
            historicos = []
            for historico in query_historico:
                historicos.append({
                    "id_profissional":historico.id_profissional,
                    "data_procedimento":historico.data_procedimento,
                    "id_tipo_procedimento":historico.id_tipo_procedimento,
                    "id_equipamento":historico.id_equipamento,
                })
            historico_completo["procedimentos"] = historicos
    except Exception as err:
        print(err)
        return{"sucess":False, "message": "Falha ao encontrar o histórico médico!"}, 400
    try:
        query_exame = banco.session.query(exames.Exame).where(exames.Exame.id_paciente==cpf).all()
        if query_exame:
            historicos = []
            for historico in query_exame:
                historicos.append({
                "tipo_exame":historico.tipo_exame,
                "descricao_exame":historico.descricao_exame,
                "data_solicitacao":historico.data_solicitacao,
                "data_realizacao":historico.data_realizacao,
                "laudo_medico":historico.laudo_medico,
                "status_exame":historico.status_exame,
                "resultado_exame":historico.resultado_exame
            })
            historico_completo["exames"] = historicos
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao encontrar o exame!"}, 400
    try:
        query_prontuario = banco.session.query(Prontuario).where(Prontuario.id_paciente==cpf).all()
        if query_prontuario:
            historicos = []
            for historico in query_prontuario:
                historicos.append({
                    "data_entrada":historico.data_entrada,
                    "medico_responsavel":historico.medico_responsavel,
                    "descricao":historico.descricao
                })
            historico_completo["prontuarios"] = historicos
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao encontrar o prontuário!"}, 400
    return{"sucess":True, "message": "Histórico completo encontrado!", "historico":historico_completo}, 201





# Medicamentos em uso pelo paciente
@pacientes.route("/medicamentos_em_uso", methods=["GET"])
def medicamentos_em_uso():
    cpf = request.form.get("cpf")
    if not cpf:
        return{"sucess":False, "message": " CPF é obrigatório!"}, 400
    medicamento_historico = {}
    try:
        query_medicamento = banco.session.query(medicamentos.Medicamento).where(medicamentos.Medicamento.id_medicamento==cpf).all()
        historicos = []
        for historico in query_medicamento:
            historicos.append({
                "id_medicamento":historico.id_medicamento,
                "nome_medicamento":historico.nome_medicamento,
                "dosagem":historico.dosagem,
                "data_validade":historico.data_validade,
                "fabricante":historico.fabricante,
                "preco_unitario":historico.preco_unitario
            })
            data_validade = datetime.strptime(data_validade, "%d/%m/%Y")
            medicamento_historico["medicamentos"] = historicos
    except Exception as err:
        print(err)
        banco.session.rollback()
        return{"sucess":False, "message": "Falha ao encontrar o medicamento!"},








# Histórico de cirurgias do paciente
@pacientes.route("/cirurgia_paciente", methods=["GET"])
def cirurgias_paciente():
    id_cirurgia = 1  # ID fixo representando cirurgias
    id_paciente = request.form.get("cpf")
    try:
        query_cirurgia = banco.session.query(procedimentos.Procedimento).where(procedimentos.Procedimento.id_paciente==id_paciente).where(procedimentos.Procedimento.id_tipo_procedimento==id_cirurgia).all()
        if not query_cirurgia:
            return{"sucess":False, "message": "Nenhuma cirurgia cadastrada!"}, 400
        cirurgias = []
        for cirurgia in query_cirurgia:
            cirurgias.append(cirurgia)
        return{"sucess":True, "message": "Cirurgias encontradas!", "cirurgias": cirurgias}, 201
    except Exception as err:
        return{"sucess":False, "message": "Cirurgia encontrada com sucesso!"}, 201

# Contato de emergência do paciente
@pacientes.route("/contato_emergencia", methods=["GET"])
def contato_emergencia():
    cpf = request.form.get("cpf")
    if not cpf:
        return{"sucess":False, "message": "CPF é obrigatório!"}, 400
    try:
        query_paciente = banco.session.query(paciente_db.Paciente).where(paciente_db.Paciente.cpf==cpf).first()
        if not query_paciente:
            banco.session.commit()
            return{"sucess":False, "message": "Telefone não cadastrado!"}, 400
        telefone_contato = query_paciente.telefone_contato
        return{"sucess":True, "message": "Telefone encontrado com sucesso!", "telefone_contato":telefone_contato}, 201
    except Exception as err:
        return{"sucess":False, "message": "Falha ao encontrar o telefone!"}, 400
