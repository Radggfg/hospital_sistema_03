import sqlalchemy  # Importa o módulo principal do SQLAlchemy.

from sqlalchemy import orm, Enum  # Importa funcionalidades do ORM e o tipo Enum (embora não utilizado aqui).

from . import Base  # Importa a classe base dos modelos ORM (declarative_base).

# ------------------- MODELO DE ESCALAS TRABALHISTAS -------------------

class Escala_Trabalhista(Base):
    __tablename__ = "Escalas_Trabalhistas"  # Define o nome da tabela no banco.

    id_profissional = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))
    # Chave estrangeira que associa a escala a um profissional da equipe.

    periodo_inicio = sqlalchemy.Column(sqlalchemy.Time())
    # Horário de início da jornada de trabalho.

# Define a coluna 'data_escala_inicio' como do tipo Date (apenas data, sem hora).
# Essa coluna armazena a data de início da escala de trabalho ou de um período de plantão.
# Exemplo de valor: 2025-05-01
    data_escala_inicio = sqlalchemy.Column(sqlalchemy.Date())

# Define a coluna 'data_escala_fim' também como do tipo Date.
# Essa coluna armazena a data de término da escala de trabalho ou período de plantão.
# Exemplo de valor: 2025-05-07
    data_escala_fim = sqlalchemy.Column(sqlalchemy.Date())

    periodo_fim = sqlalchemy.Column(sqlalchemy.Time())
    # Horário de término da jornada de trabalho.

    tipo_turno = sqlalchemy.Column(sqlalchemy.String(255))
    # Descreve o tipo de turno (ex: "manhã", "noite", "plantão 12x36").

    id_setor = sqlalchemy.Column(sqlalchemy.INT)
    # Identificador do setor/hospital onde o profissional está atuando.

    id_escala = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária da escala. Identifica unicamente cada escala cadastrada.

# ------------------- MODELO DE FLUXO DE HORÁRIO -------------------

class Fluxo_Horario(Base):
    __tablename__ = "Fluxos_Horarios"  # Nome da tabela no banco.

    id_fluxo = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária do fluxo de horário, identificador único.

    id_profissional = sqlalchemy.Column(sqlalchemy.String(100))
    # ID do profissional (não é FK aqui, mas poderia ser para mais consistência).

    data_movimentacao = sqlalchemy.Column(sqlalchemy.Date())
    # Data da movimentação (entrada e saída) registrada.

    hora_entrada = sqlalchemy.Column(sqlalchemy.Time())
    # Horário de entrada real do profissional.

    hora_saida = sqlalchemy.Column(sqlalchemy.Time())
    # Horário de saída real do profissional.

    id_setor = sqlalchemy.Column(sqlalchemy.INT)
    # ID do setor onde ocorreu a movimentação.

    id_escala = sqlalchemy.Column(sqlalchemy.ForeignKey("Escalas_Trabalhistas.id_escala"))
    # Chave estrangeira ligando esse fluxo à escala planejada correspondente.

# ------------------- MODELO DE JUSTIFICATIVAS DE AUSÊNCIA -------------------

