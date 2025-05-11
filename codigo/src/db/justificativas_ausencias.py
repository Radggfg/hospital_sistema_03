# Importa o módulo SQLAlchemy, necessário para definir modelos ORM e interações com o banco de dados
import sqlalchemy  

# Importa o objeto Base do módulo atual, que é geralmente uma instância de declarative_base()
# Base é a classe base para todos os modelos declarativos no SQLAlchemy
from . import Base  

# Define a classe Justificativa_ausencia como uma subclasse de Base.
# Essa classe representa a tabela 'Justificativas_Ausencias' no banco de dados.
class Justificativa_ausencia(Base):  
    # Define o nome da tabela no banco de dados como 'Justificativas_Ausencias'
    __tablename__ = "Justificativas_Ausencias"

    # Define a coluna 'id_justificativa' como chave primária (primary key) do tipo inteiro
    id_justificativa = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)

    # Define a coluna 'id_profissional' como um inteiro simples (não é definida como chave estrangeira aqui)
    id_profissional = sqlalchemy.Column(sqlalchemy.INT)

    # Define a coluna 'data_ausencia' como um DateTime, para armazenar a data e hora da ausência
    data_ausencia = sqlalchemy.Column(sqlalchemy.DateTime())

    # Define a coluna 'motivo_ausencia' como uma string com limite de 255 caracteres
    motivo_ausencia = sqlalchemy.Column(sqlalchemy.String(255))

    # Define a coluna 'status_justificativa' para armazenar o status (ex: aprovada, pendente, negada)
    status_justificativa = sqlalchemy.Column(sqlalchemy.String(255))

    # Define a coluna 'documento_justificativa' para armazenar o nome ou caminho de um arquivo comprobatório
    documento_justificativa = sqlalchemy.Column(sqlalchemy.String(255))

    # Define 'id_escala' como uma chave estrangeira que referencia 'id_escala' na tabela 'Escalas_Trabalhista'
    id_escala = sqlalchemy.Column(sqlalchemy.ForeignKey("Escalas_Trabalhistas.id_escala"))
