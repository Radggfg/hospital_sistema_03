import sqlalchemy  # Importa o SQLAlchemy para trabalhar com bancos de dados relacionais.
from sqlalchemy import orm, Enum  # Importa funcionalidades do ORM e tipo Enum (não usado aqui, mas útil para enumerações).
from . import Base  # Importa a base declarativa para criar os modelos ORM.

# ------------------------ MODELO DE PERMISSÕES DO SISTEMA ------------------------

class Permissao(Base):
    __tablename__ = "permissoes"  # Nome da tabela no banco.

    id_permissao = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único da permissão (chave primária).

    nome_permissao = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome da permissão (ex: "acesso_admin", "editar_usuarios").

    descricao = sqlalchemy.Column(sqlalchemy.TEXT)
    # Descrição detalhada do que a permissão permite fazer.

    nivel_acesso = sqlalchemy.Column(sqlalchemy.INT)
    # Nível hierárquico da permissão (ex: 1 = básico, 5 = total).

    status_ativo = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    # Indica se a permissão está ativa ou inativa.

    criado_em = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data/hora de criação da permissão.

    atualizado_em = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data/hora da última atualização da permissão.

# ------------------------ VÍNCULO ENTRE FUNCIONÁRIO E PERMISSÃO ------------------------

class Funcionario_Permissao(Base):
    __tablename__ = "funcionarios_permissoes"  # Nome da tabela de relacionamento.

    id_permissao_funcionario = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único da permissão aplicada ao funcionário.

    nome_permissao = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome da permissão atribuída (repete de forma desnormalizada o nome da permissão).

    descricao = sqlalchemy.Column(sqlalchemy.TEXT)
    # Descrição da permissão atribuída (também desnormalizada).

    setor_destinado = sqlalchemy.Column(sqlalchemy.String(100))
    # Setor para o qual a permissão se destina (ex: "RH", "Financeiro", "TI").

    funcao_destinada = sqlalchemy.Column(sqlalchemy.String(100))
    # Função específica (ex: "coordenador", "analista").

    status_ativo = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    # Indica se a permissão está ativa para o funcionário.

    criado_em = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data/hora de criação do vínculo permissão-funcionário.

    atualizado_em = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data/hora da última atualização do vínculo.

    id_permissao = sqlalchemy.Column(sqlalchemy.ForeignKey("Permissoes.id_permissao"))
    # Chave estrangeira que liga à tabela de permissões.

    cpf = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))
    # Chave estrangeira que liga ao profissional que recebeu essa permissão.





