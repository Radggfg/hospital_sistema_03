import sqlalchemy  # Importa o módulo principal do SQLAlchemy, com suporte a tipos de dados e definição de colunas.

from sqlalchemy import orm, Enum  # Importa ferramentas do ORM e o tipo de dado Enum (usado para tipo sanguíneo).

from . import Base  # Importa a classe base dos modelos ORM, que define o mapeamento com o banco de dados.

class Diagnostico(Base):  # Define o modelo Diagnostico como uma tabela ORM.
    __tablename__ = "Diagnosticos"  # Define o nome da tabela no banco de dados como 'Diagnosticos'.

    tipo_sanguineo = sqlalchemy.Column(sqlalchemy.Enum(
        'A+','A-','B+','B-','AB+','AB-','O+','O-'
    ))
    # Coluna com tipo enumerado para armazenar o tipo sanguíneo do paciente relacionado ao diagnóstico.
    # Usa valores pré-definidos para garantir consistência dos dados.

    descricao = sqlalchemy.Column(sqlalchemy.Text())
    # Campo de texto livre para descrever o diagnóstico médico do paciente.
    # Pode conter observações clínicas, hipóteses ou laudos.

    id_diagnostico = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária que identifica unicamente cada diagnóstico.
