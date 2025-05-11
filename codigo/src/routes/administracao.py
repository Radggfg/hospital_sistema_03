from flask import Blueprint, request
# Importa os módulos do Flask necessários:
# - Blueprint: permite modularizar as rotas da aplicação em diferentes arquivos.
# - request: utilizado para acessar os dados enviados em requisições HTTP (como formulários ou JSON).

from src import banco
# Importa a instância do banco de dados (normalmente um objeto SQLAlchemy) que será usada para sessões de transação, commit e rollback.

from src.db import departamentos, permissoes
# Importa os modelos ORM relacionados ao banco de dados:
# - departamentos: contém a classe Departamento usada nas operações de CRUD.
# - permissoes: contém as classes Permissao e Funcionario_Permissao.

from datetime import datetime
# Importa a classe datetime do Python, utilizada para manipulação de datas e horários (ex: registrar criação ou atualização de registros).

# Blueprint para rotas do módulo de administração
administracao = Blueprint("administracao", __name__, url_prefix="/administracao")

# -------------------- DEPARTAMENTOS --------------------

# Listar todos os departamentos cadastrados
@administracao.route("/listar_departamento", methods=["GET"])
def listar_departamentos():
    todos_departamentos = departamentos.Departamento.query.all()
    return {"sucess": True, "todos_departamentos": todos_departamentos}

# Adicionar um novo departamento ao sistema
@administracao.route("/adicionar_departamento", methods=["POST"])
def adicionar_departamento():
    nome = request.form.get("nome")
    sigla = request.form.get("sigla")
    andar_localizacao = request.form.get("andar_localizacao")
    ramal_telefone = request.form.get("ramal_telefone")
    email = request.form.get("email")
    id_responsavel = request.form.get("id_responsavel")
    status = request.form.get("status")

    # Verifica se todos os campos obrigatórios foram preenchidos
    if not nome or not andar_localizacao or not ramal_telefone or not email or not id_responsavel or not status:
        return {"sucess": False, "message": "Campos obrigatórios estão faltando!"}, 400

    novo_departamento = departamentos.Departamento(
        nome=nome,
        sigla=sigla,
        andar_localizacao=andar_localizacao,
        ramal_telefone=ramal_telefone,
        email=email,
        id_responsavel=id_responsavel,
        status=status
    )

    try:
        banco.session.add(novo_departamento)
        banco.session.commit()
        return {"sucess": True, "message": "Departamento cadastrado!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao cadastrar o departamento!"}, 400

# Editar um departamento existente
@administracao.route("/editar_departamento", methods=["PUT"])
def editar_departamento():
    id_departamento = request.form.get("id_departamento")
    if not id_departamento:
        return {"sucess": False, "message": "id_departamento é obrigatório!"}, 400

    # Campos a serem atualizados
    novo_andar_localizacao = request.form.get("andar_localizacao")
    novo_ramal_telefone = request.form.get("ramal_telefone")
    novo_email = request.form.get("email")
    novo_id_responsavel = request.form.get("id_responsavel")
    novo_status = request.form.get("status")

    try:
        query = banco.session.query(departamentos.Departamento).filter_by(id_departamento=id_departamento).first()

        # Atualiza somente os campos informados
        if novo_andar_localizacao:
            query.andar_localizacao = novo_andar_localizacao
        if novo_ramal_telefone:
            query.ramal_telefone = novo_ramal_telefone
        if novo_email:
            query.email = novo_email
        if novo_id_responsavel:
            query.id_responsavel = novo_id_responsavel
        if novo_status:
            query.status = novo_status

        banco.session.commit()
        return {"sucess": True, "message": "Departamento atualizado com sucesso!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao atualizar o departamento!"}, 400

# Remover um departamento do sistema
@administracao.route("/deletar_departamento", methods=["DELETE"])
def deletar_departamento():
    id_departamento = request.form.get("id_departamento")
    query = banco.session.query(departamentos.Departamento).filter_by(id_departamento=id_departamento).first()

    try:
        banco.session.delete(query)
        banco.session.commit()
        return {"sucess": True, "message": "Departamento deletado com sucesso!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Falha ao deletar o departamento!"}, 400

# -------------------- PERMISSÕES --------------------

# Criar nova permissão de sistema
@administracao.route("/criar_permissao", methods=["POST"])
def criar_permissao():
    nome_permissao = request.form.get("nome_permissao")
    descricao = request.form.get("descricao")
    nivel_acesso = request.form.get("nivel_acesso")
    status_ativo = request.form.get("status_ativo")

    if not nome_permissao or not descricao or not nivel_acesso or not status_ativo:
        return {"sucess": False, "message": "Campos obrigatórios estão faltando!"}, 400

    nova = permissoes.Permissao(
        nome_permissao=nome_permissao,
        descricao=descricao,
        nivel_acesso=nivel_acesso,
        status_ativo=status_ativo
    )

    try:
        banco.session.add(nova)
        banco.session.commit()
        return {"sucess": True, "message": "Permissão criada com sucesso!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Erro ao criar a permissão."}, 400

# Atribuir permissão a um funcionário
@administracao.route("/atribuir_permissao", methods=["POST"])
def criar_permissao_funcionario():
    id_permissao = request.form.get("id_permissao")
    cpf = request.form.get("cpf")
    setor_destinado = request.form.get("setor_destinado")
    status_ativo = request.form.get("status_ativo")

    if not id_permissao or not cpf or not setor_destinado or not status_ativo:
        return {"sucess": False, "message": "Campos obrigatórios estão faltando!"}, 400

    nova = permissoes.Funcionario_Permissao(
        id_permissao=id_permissao,
        cpf=cpf,
        setor_destinado=setor_destinado,
        status_ativo=status_ativo
    )

    try:
        banco.session.add(nova)
        banco.session.commit()
        return {"sucess": True, "message": "Permissão atribuída ao funcionário!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Erro ao atribuir permissão."}, 400

# Atualizar status da permissão
@administracao.route("/alterar_permissao", methods=["PUT"])
def alterar_permissoes():
    id_permissao = request.form.get("id_permissao")
    novo_status = request.form.get("alteracao")

    if not id_permissao or not novo_status:
        return {"sucess": False, "message": "id_permissao e novo_status são obrigatórios!"}, 400

    try:
        query = banco.session.query(permissoes.Permissao).filter_by(id_permissao=id_permissao).first()
        query.status_ativo = novo_status
        banco.session.commit()
        return {"sucess": True, "message": "Permissão atualizada com sucesso!"}, 201
    except Exception:
        banco.session.rollback()
        return {"sucess": False, "message": "Erro ao atualizar permissão."}, 400
