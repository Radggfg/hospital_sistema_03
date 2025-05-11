import sqlalchemy  # Importa o módulo base do SQLAlchemy.
from sqlalchemy import orm, Enum  # Importa ORM e suporte a Enum (caso necessário).
from . import Base  # Importa a classe base para os modelos ORM.

# ------------------------------ MODELO PROCEDIMENTO ------------------------------

class Procedimento(Base):
    __tablename__ = "Procedimentos"  # Nome da tabela no banco de dados.

    id_procedimento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária que identifica de forma única o procedimento realizado.

    id_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Pacientes.cpf"))
    # Chave estrangeira que relaciona o procedimento ao paciente.

    id_profissional = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))
    # Chave estrangeira para o profissional responsável pela execução do procedimento.

    data_procedimento = sqlalchemy.Column(sqlalchemy.DateTime)
    # Data e hora em que o procedimento foi realizado.

    id_especialidade = sqlalchemy.Column(sqlalchemy.INT)
    # ID da especialidade relacionada ao procedimento.
    # (Sugestão: transformar em ForeignKey se houver uma tabela de especialidades)

    id_recebimento_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Recebimentos_Pacientes.id_recebimento_paciente"))
    # Chave estrangeira para o recebimento financeiro associado ao procedimento (se aplicável).

    id_despesa_hospitalar = sqlalchemy.Column(sqlalchemy.ForeignKey("Despesas_Hospitalares.id_despesa_hospitalar"))
    # Chave estrangeira que liga o procedimento a um custo registrado nas despesas hospitalares.

    id_tipo_procedimento = sqlalchemy.Column(sqlalchemy.ForeignKey("Tipos_procedimentos.id_tipo_procedimento"))
    # Chave estrangeira para o tipo do procedimento (ex: cirurgia, curativo, avaliação, etc.).

    id_equipamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Equipamentos.id_equipamento"))
    # Chave estrangeira para o equipamento utilizado no procedimento (se houve uso).
