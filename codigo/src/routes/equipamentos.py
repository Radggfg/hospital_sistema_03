from flask import Blueprint, request  # Importa os módulos necessários do Flask
from src import banco  # Importa a sessão do banco de dados
from src.db import paciente, consultas, profissional, prontuarios, exames, equipamentos  # Importa os modelos utilizados
from datetime import datetime, timedelta  # Para manipulação de datas
from dateutil.relativedelta import relativedelta  # Para cálculo de validade com base em anos
from sqlalchemy import select  # Utilizado para montar queries seguras

# Cria o blueprint para o módulo de equipamentos
equipamento = Blueprint("equipamento", __name__, url_prefix="/equipamento")

# ---------------------- Cadastrar equipamento ----------------------
@equipamento.route("/cadastrar_equipamento", methods=["PUT"])
def cadastrar_equipamento():
    # Coleta dados do formulário
    nome_equipamento = request.form.get("nome_equipamento")
    categoria = request.form.get("categoria")
    data_aquisicao = request.form.get("data_aquisicao")
    custo_base = request.form.get("custo_base")
    custo_manutencao = request.form.get("custo_manutencao")
    setor = request.form.get("setor")
    fabricante = request.form.get("fabricante")
    modelo = request.form.get("modelo")
    numero_serie = request.form.get("numero_serie")
    vida_util = request.form.get("vida_util")
    estado_atual = request.form.get("estado_atual")

    # Converte data
    data_aquisicao = datetime.strptime(data_aquisicao, "%d/%m/%Y")

    # Validação de campos obrigatórios
    if not nome_equipamento or not categoria or not data_aquisicao or not custo_base or not custo_manutencao or not setor or not fabricante or not modelo or not numero_serie or not vida_util or not estado_atual:
        return {"sucess": False, "message": "Campos obrigatórios estão faltando!"}, 400

    # Cria novo objeto
    novo_equipamento = equipamentos.Equipamento(
        nome_equipamento=nome_equipamento,
        categoria=categoria,
        data_aquisicao=data_aquisicao,
        custo_base=custo_base,
        custo_manutencao=custo_manutencao,
        setor=setor,
        fabricante=fabricante,
        modelo=modelo,
        numero_serie=numero_serie,
        vida_util=vida_util,
        estado_atual=estado_atual
    )

    # Tenta inserir no banco
    try:
        banco.session.add(novo_equipamento)
        banco.session.commit()
        return {"sucess": True, "message": "Equipamento cadastrado!"}, 201
    except Exception as err:
        banco.session.rollback()
        print(err)
        return {"sucess": False, "message": "Erro ao cadastrar equipamento."}, 400

# ---------------------- Tempo de uso ----------------------
@equipamento.route("/tempo_uso", methods=["GET"])
def tempo_uso_equipamento():
    id_equipamento = request.form.get("id_equipamento")
    utensilios_query = select(equipamentos.Equipamento.data_aquisicao).where(equipamentos.Equipamento.id_equipamento == id_equipamento)
    todos_utensilios = banco.session.execute(utensilios_query).first()

    # Calcula diferença entre hoje e aquisição
    data_atual = datetime.now()
    data_aquisicao = todos_utensilios.data_aquisicao
    tempo_uso = data_atual - data_aquisicao

    return {"sucess": True, "message": "Tempo de uso calculado.", "tempo_uso": str(tempo_uso)}

# ---------------------- Validade de equipamentos ----------------------
@equipamento.route("/validade_equipamento", methods=["GET"])
def validade_equipamento():
    utensilios_query = select(
        equipamentos.Equipamento.data_aquisicao,
        equipamentos.Equipamento.vida_util,
        equipamentos.Equipamento.estado_atual,
        equipamentos.Equipamento.id_equipamento
    )
    todos_utensilios = banco.session.execute(utensilios_query).all()
    lista = []
    for utensilio in todos_utensilios:
        validade = utensilio.data_aquisicao + relativedelta(years=utensilio.vida_util)
        lista.append({
            "id_equipamento": utensilio.id_equipamento,
            "estado_atual": utensilio.estado_atual,
            "validade": validade
        })
    return {"sucess": True, "todos_utensilios": lista}

# ---------------------- Listar equipamentos ----------------------
@equipamento.route("/listar_equipamento", methods=["GET"])
def listar_equipamentos():
    query = select(
        equipamentos.Equipamento.id_equipamento,
        equipamentos.Equipamento.descricao,
        equipamentos.Equipamento.nome_equipamento,
        equipamentos.Equipamento.categoria,
        equipamentos.Equipamento.custo_base,
        equipamentos.Equipamento.custo_manutencao,
        equipamentos.Equipamento.setor,
        equipamentos.Equipamento.fabricante,
        equipamentos.Equipamento.modelo,
        equipamentos.Equipamento.numero_serie,
        equipamentos.Equipamento.vida_util,
        equipamentos.Equipamento.estado_atual,
        equipamentos.Equipamento.data_aquisicao,
        equipamentos.Equipamento.fornecedor,
        equipamentos.Equipamento.despesa_hospitalar
    )
    todos = banco.session.execute(query).all()
    lista = []
    for utensilio in todos:
        lista.append({
            "id_equipamento": utensilio.id_equipamento,
            "descricao": utensilio.descricao,
            "nome_equipamento": utensilio.nome_equipamento,
            "categoria": utensilio.categoria,
            "custo_base": utensilio.custo_base,
            "custo_manutencao": utensilio.custo_manutencao,
            "setor": utensilio.setor,
            "fabricante": utensilio.fabricante,
            "modelo": utensilio.modelo,
            "numero_serie": utensilio.numero_serie,
            "vida_util": utensilio.vida_util,
            "estado_atual": utensilio.estado_atual,
            "data_aquisicao": utensilio.data_aquisicao,
            "fornecedor": utensilio.fornecedor,
            "despesa_hospitalar": utensilio.despesa_hospitalar
        })
    return {"sucess": True, "todos_equipamentos": lista}

# ---------------------- Atualizar equipamento ----------------------
@equipamento.route("/atualizar_equipamento", methods=["PUT"])
def atualizar_equipamento():
    id_equipamento = request.form.get("id_equipamento")
    if not id_equipamento:
        return {"sucess": False, "message": "id_equipamento é obrigatório!"}, 400

    # Novos dados opcionais
    novo_estado_atual = request.form.get("estado_atual")
    novo_custo_manutencao = request.form.get("custo_manutencao")
    novo_custo_base = request.form.get("custo_base")
    novo_modelo = request.form.get("modelo")
    nova_vida_util = request.form.get("vida_util")

    try:
        query = banco.session.query(equipamentos.Equipamento).where(equipamentos.Equipamento.id_equipamento == id_equipamento).first()
        if novo_estado_atual:
            query.estado_atual = novo_estado_atual
        if novo_custo_manutencao:
            query.custo_manutencao = novo_custo_manutencao
        if novo_custo_base:
            query.custo_base = novo_custo_base
        if novo_modelo:
            query.modelo = novo_modelo
        if nova_vida_util:
            query.vida_util = nova_vida_util
        banco.session.commit()
        return {"sucess": True, "message": "Equipamento atualizado com sucesso!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Erro ao atualizar equipamento."}, 400

# ---------------------- Deletar equipamento ----------------------
@equipamento.route("/deletar_equipamento", methods=["DELETE"])
def deletar_equipamento():
    id_equipamento = request.form.get("id_equipamento")
    query = banco.session.query(equipamentos.Equipamento).where(equipamentos.Equipamento.id_equipamento == id_equipamento).first()
    try:
        banco.session.delete(query)
        banco.session.commit()
        return {"sucess": True, "message": "Equipamento deletado com sucesso!"}, 201
    except Exception as err:
        banco.session.rollback()
        return {"sucess": False, "message": "Erro ao deletar equipamento."}, 400

# ---------------------- Buscar equipamentos por local ----------------------
@equipamento.route("/buscar_por_local", methods=["GET"])
def buscar_por_local():
    setor = request.form.get("setor")
    if not setor:
        return {"sucess": False, "message": "Setor é obrigatório!"}, 400
    try:
        todos_locais = banco.session.query(equipamentos.Equipamento).where(equipamentos.Equipamento.setor == setor).all()
        lista = []
        for local in todos_locais:
            lista.append({
                "descricao": local.descricao,
                "nome_equipamento": local.nome_equipamento,
                "categoria": local.categoria,
                "setor": local.setor,
                "modelo": local.modelo,
                "numero_serie": local.numero_serie,
                "data_aquisicao": local.data_aquisicao,
                "estado_atual": local.estado_atual
            })
        return {"sucess": True, "todos_locais": lista}
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Erro ao buscar por local."}, 400
