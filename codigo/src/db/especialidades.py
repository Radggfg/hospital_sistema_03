import sqlalchemy  # Importa o módulo principal do SQLAlchemy, que fornece os tipos de dados e funcionalidades ORM.

from sqlalchemy import orm, Enum  # Importa o ORM e o tipo Enum (apesar de não usado neste modelo).

from . import Base  # Importa a classe base dos modelos (criada com declarative_base).

class Especialidade(Base):  # Define o modelo ORM para a tabela de especialidades médicas ou profissionais.
    __tablename__ = "Especialidades"  # Define o nome da tabela no banco como 'Especialidades'.

    id_especialidade = orm.mapped_column(sqlalchemy.INT, primary_key=True)
    # Chave primária da especialidade. Identificador único usado em relacionamentos com outros modelos (como Profissional).

    nome_especialidade = orm.mapped_column(sqlalchemy.String(100))
    # Nome da especialidade (ex: "Cardiologia", "Ortopedia", "Pediatria").
