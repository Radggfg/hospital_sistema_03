import sqlalchemy  # Importa o SQLAlchemy para definição de tipos e estrutura do banco.
from sqlalchemy import orm, Enum  # ORM e suporte para tipos enumerados.
from .especialidades import Especialidade  # Importa o modelo de especialidade (relacionamento direto).
from . import Base  # Importa a base declarativa para herança nos modelos ORM.

# ----------------------------- MODELO PROFISSIONAL -----------------------------

class Profissional(Base):
    __tablename__ = "Profissionais"  # Nome da tabela no banco de dados.

    nome = orm.mapped_column(sqlalchemy.String(100))
    # Nome completo do profissional de saúde.

    email = orm.mapped_column(sqlalchemy.String(100))
    # E-mail de contato institucional ou pessoal.

    id_especialidade = orm.mapped_column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Especialidades.id_especialidade"))
    # Chave estrangeira para a tabela de Especialidades (ex: Cardiologia, Pediatria).

    cargo = orm.mapped_column(sqlalchemy.String(100))
    # Cargo ocupado pelo profissional (ex: Médico, Enfermeiro, Técnico).

    cod_registro = orm.mapped_column(sqlalchemy.String(15))
    # Código de registro profissional (ex: CRM, COREN, CRO).

    cpf = orm.mapped_column(sqlalchemy.String(100), primary_key=True)
    # CPF como identificador único do profissional (chave primária).

    carteira_trabalho = orm.mapped_column(sqlalchemy.String(15))
    # Número da carteira de trabalho.

    departamento = orm.mapped_column(sqlalchemy.String(100))
    # Departamento onde o profissional atua (ex: UTI, Clínico Geral, Cirurgia).

    data_nascimento = orm.mapped_column(sqlalchemy.Date)
    # Data de nascimento do profissional.

    status = orm.mapped_column(sqlalchemy.Enum('ativo','afastado','licença','férias'))
    # Status atual do profissional no hospital ou clínica.


# ------------------------ MODELO PROFISSIONAL_LEITO ------------------------

class Profissional_Leito(Base):
    __tablename__ = "Profissionais_Leitos"  # Tabela que vincula profissionais a leitos.

    id_profissional_leito = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único da relação entre profissional e leito.

    id_profissional = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))
    # Chave estrangeira para o CPF do profissional.

    id_leito = sqlalchemy.Column(sqlalchemy.ForeignKey("Leitos.id_leito"))
    # Chave estrangeira para o leito atribuído ao profissional.

    data_atribuicao = sqlalchemy.Column(sqlalchemy.Date())
    # Data em que o profissional foi designado ao leito.

    turno = sqlalchemy.Column(sqlalchemy.Enum('Manhã','Tarde','Noite','Plantão 24h'))
    # Turno em que o profissional está responsável pelo leito.

    status = sqlalchemy.Column(sqlalchemy.Enum('Ativo','Inativo'))
    # Status da designação (ativa ou finalizada).

    observacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Campo livre para anotações adicionais sobre a atribuição (ex: substituições, motivos específicos).
