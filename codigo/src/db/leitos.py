import sqlalchemy  # Importa o módulo principal do SQLAlchemy, com tipos e funções para manipular o banco.

from sqlalchemy import orm, Enum  # Importa funcionalidades do ORM e o tipo Enum para valores controlados.

from . import Base  # Importa a classe base dos modelos ORM.

class Leito(Base):  # Define o modelo Leito, que representa os leitos disponíveis no hospital.
    __tablename__ = "Leitos"  # Nome da tabela no banco de dados.

    id_leito = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único de cada leito — chave primária da tabela.

    numero_sala = sqlalchemy.Column(sqlalchemy.INT)
    # Número da sala onde o leito está localizado (ex: sala 203).

    andar_sala = sqlalchemy.Column(sqlalchemy.INT)
    # Andar do hospital em que o leito está localizado (ex: 2º andar).

    tipo_leito = sqlalchemy.Column(sqlalchemy.Enum(
        'ENFERMARIA', 'APARTAMENTO', 'UTI_ADULTO', 'UTI_PEDIATRICA', 'UTI_NEONATAL', 'ISOLAMENTO'
    ))
    # Tipo de leito, com opções controladas por Enum.
    # Isso ajuda na organização e distribuição de pacientes conforme a gravidade e necessidade.

    status = sqlalchemy.Column(sqlalchemy.Enum(
        'DISPONIVEL', 'OCUPADO', 'MANUTENCAO', 'RESERVADO'
    ), default='DISPONÍVEL')
    # Situação atual do leito. O valor padrão é 'DISPONÍVEL'.
    # Ajuda no controle operacional do setor hospitalar.

    periodo_ocupacao = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data e hora da ocupação atual do leito (se estiver ocupado).
    # Pode ser usado para calcular tempo de uso ou prever liberação.

    responsavel = sqlalchemy.Column(sqlalchemy.String(255))
    # Nome do profissional ou equipe responsável pelo leito.
    # Pode representar enfermeiros, equipe de limpeza, médico responsável etc.
