# Importações necessárias para o uso de rotas e manipulação de requisições
from flask import Blueprint
from flask import request
from src import banco  # Importa o banco de dados configurado na aplicação
from src.db import paciente, consultas, profissional, prontuarios, exames, equipamentos  # Tabelas do banco
from datetime import datetime  # Para manipulação de datas
from sqlalchemy import select  # Para realizar consultas SELECT
from src.db import fornecedores as fornecedor_db  # Importa o modelo da tabela de fornecedores com alias

# Define um Blueprint para agrupar as rotas relacionadas aos fornecedores
fornecedor = Blueprint("fornecedor", __name__, url_prefix="/fornecedor")

# Rota para cadastrar um novo fornecedor
@fornecedor.route("/cadastrar_fornecedor", methods=["POST"])
def cadastrar_fornecedor():
    # Coleta os dados enviados no corpo da requisição
    nome_fornecedor = request.form.get("nome_fornecedor")
    cnpj = request.form.get("cnpj")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    endereco = request.form.get("endereco")
    cidade = request.form.get("cidade")
    estado = request.form.get("estado")
    tipo_fornecedor = request.form.get("tipo_fornecedor")

    # Validação obrigatória para todos os campos
    if not nome_fornecedor or not cnpj or not telefone or not email or not endereco or not cidade or not estado or not tipo_fornecedor:
        return {"sucess": False, "message": "nome_fornecedor, cnpj, telefone, email, endereco, cidade e tipo_fornecedor são obrigatórios!"}, 400

    # Criação do novo objeto fornecedor
    novo_fornecedor = fornecedor_db.Fornecedor(
        nome_fornecedor=nome_fornecedor,
        cnpj=cnpj,
        telefone=telefone,
        email=email,
        endereco=endereco,
        cidade=cidade,
        estado=estado,
        tipo_fornecedor=tipo_fornecedor,
    )

    # Tenta adicionar e salvar no banco
    try:
        banco.session.add(novo_fornecedor)
        banco.session.commit()
        return {"sucess": True, "message": "Fornecedor cadastrado!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao cadastrar o fornecedor!"}, 400

# Rota para listar todos os fornecedores
@fornecedor.route("/listar_fornecedor", methods=["GET"])
def listar_fornecedores():
    # Monta a query de seleção dos campos desejados
    fornecedores_query = select(
        fornecedor_db.Fornecedor.nome_fornecedor,
        fornecedor_db.Fornecedor.cnpj,
        fornecedor_db.Fornecedor.telefone,
        fornecedor_db.Fornecedor.email,
        fornecedor_db.Fornecedor.endereco,
        fornecedor_db.Fornecedor.cidade,
        fornecedor_db.Fornecedor.estado,
        fornecedor_db.Fornecedor.tipo_fornecedor,
        fornecedor_db.Fornecedor.data_cadastro
    )
    # Executa a query
    todos_fornecedores = banco.session.execute(fornecedores_query).all()

    # Transforma o resultado em lista de dicionários
    lista = []
    for fornecedor in todos_fornecedores:
        lista.append({
            "nome_fornecedor": fornecedor.nome_fornecedor,
            "cnpj": fornecedor.cnpj,
            "telefone": fornecedor.telefone,
            "email": fornecedor.email,
            "endereco": fornecedor.endereco,
            "cidade": fornecedor.cidade,
            "estado": fornecedor.estado,
            "tipo_fornecedor": fornecedor.tipo_fornecedor,
            "data_cadastro": fornecedor.data_cadastro
        })

    return {"sucess": True, "todos_fornecedores": lista}

# Rota para atualizar os dados de um fornecedor
@fornecedor.route("/atualizar_fornecedor", methods=["PUT"])
def atualizar_fornecedor():
    # Busca o fornecedor pelo CNPJ (chave única)
    cnpj_fornecedor = request.form.get("cnpj")
    if not cnpj_fornecedor:
        return {"sucess": False, "message": "cnpj é obrigatório!"}, 400

    # Novos valores a serem atualizados
    novo_telefone_fornecedor = request.form.get("telefone")
    novo_email_fornecedor = request.form.get("email")
    novo_endereco_fornecedor = request.form.get("endereco")
    nova_cidade_fornecedor = request.form.get("cidade")
    novo_estado_fornecedor = request.form.get("estado")

    try:
        # Busca o fornecedor existente no banco
        query_fornecedor = banco.session.query(fornecedor_db.Fornecedor).where(
            fornecedor_db.Fornecedor.cnpj == cnpj_fornecedor).first()

        # Atualiza os campos que foram enviados
        if novo_telefone_fornecedor:
            query_fornecedor.telefone = novo_telefone_fornecedor
        if novo_email_fornecedor:
            query_fornecedor.email = novo_email_fornecedor
        if novo_endereco_fornecedor:
            query_fornecedor.endereco = novo_endereco_fornecedor
        if nova_cidade_fornecedor:
            query_fornecedor.cidade = nova_cidade_fornecedor
        if novo_estado_fornecedor:
            query_fornecedor.estado = novo_estado_fornecedor

        # Salva as alterações
        banco.session.commit()
        return {"sucess": True, "message": "Fornecedor foi atualizado!"}, 201
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao atualizar o fornecedor!"}, 400

# Rota para deletar um fornecedor pelo CNPJ
@fornecedor.route("/deletar_fornecedor", methods=["DELETE"])
def deletar_fornecedor():
    cnpj = request.form.get("cnpj")
    query_fornecedor = banco.session.query(fornecedor_db.Fornecedor).where(fornecedor_db.Fornecedor.cnpj == cnpj).first()

    try:
        banco.session.delete(query_fornecedor)
        banco.session.commit()
        return {"sucess": True, "message": "Fornecedor deletado com sucesso!"}, 201
    except Exception as err:
        return {"sucess": False, "message": "Falha ao deletar o fornecedor!"}, 400

# Rota para buscar um fornecedor específico pelo nome
@fornecedor.route("/buscar_fornecedor", methods=["GET"])
def buscar_fornecedor_nome():
    nome = request.form.get("nome_fornecedor")
    if not nome:
        return {"sucess": False, "message": "Nome é obrigatório!"}, 400

    try:
        # Busca o fornecedor pelo nome
        query_fornecedor = banco.session.query(fornecedor_db.Fornecedor).where(
            fornecedor_db.Fornecedor.nome_fornecedor == nome).first()
        banco.session.commit()

        # Retorna os dados do fornecedor encontrado
        resultado = {
            "nome_fornecedor": query_fornecedor.nome_fornecedor,
            "cnpj": query_fornecedor.cnpj,
            "telefone": query_fornecedor.telefone,
            "email": query_fornecedor.email,
            "endereco": query_fornecedor.endereco,
            "cidade": query_fornecedor.cidade,
            "estado": query_fornecedor.estado,
            "tipo_fornecedor": query_fornecedor.tipo_fornecedor,
            "data_cadastro": query_fornecedor.data_cadastro
        }

        return {"sucess": True, "todos_fornecedores": resultado}
    except Exception as err:
        print(err)
        banco.session.rollback()
        return {"sucess": False, "message": "Nome do fornecedor não foi encontrado!"}, 400
