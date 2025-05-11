import sqlalchemy  # Importa o módulo principal do SQLAlchemy.
from sqlalchemy import orm, Enum  # Importa funcionalidades do ORM e suporte a enums (não utilizado aqui).
from . import Base  # Importa a base declarativa usada por todos os modelos ORM.

# ------------------------------ MODELO PRONTUÁRIO ------------------------------

class Prontuario(Base):
    __tablename__ = "Prontuarios"  # Define o nome da tabela no banco de dados.

    id_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Pacientes.cpf"))
    # Chave estrangeira que relaciona o prontuário ao paciente correspondente.

    data_entrada = sqlalchemy.Column(sqlalchemy.DateTime)
    # Data e hora de abertura do prontuário (geralmente associada à internação ou início do atendimento).

    medico_responsavel = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))
    # Chave estrangeira que identifica o profissional de saúde responsável pelo caso.

    descricao = sqlalchemy.Column(sqlalchemy.Text())
    # Campo de texto livre para descrição clínica inicial, histórico médico, anotações evolutivas, etc.

    id_prontuario = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária do prontuário. Identificador único no sistema.



