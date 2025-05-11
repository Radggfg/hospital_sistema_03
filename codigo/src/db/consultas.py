import sqlalchemy  # Importa o módulo principal do SQLAlchemy para acessar tipos de dados e colunas.

from sqlalchemy import orm, Enum  # Importa utilitários do ORM e o tipo Enum (caso deseje usar tipos enumerados mais adiante).

from . import Base  # Importa a classe base definida anteriormente (usada para mapear esta classe como uma tabela no banco de dados).

class Consulta(Base):  # Define a classe Consulta, que será mapeada como uma tabela no banco de dados.
    __tablename__ = "Consultas"  # Define o nome da tabela como 'Consultas'.

    id_consulta = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)  
    # Coluna de chave primária que identifica unicamente cada consulta.

    id_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Pacientes.cpf"))  
    # Chave estrangeira que referencia o CPF do paciente na tabela 'Pacientes'.

    id_profissional = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))  
    # Chave estrangeira que referencia o CPF do profissional na tabela 'Profissionais'.

    data_hora = sqlalchemy.Column(sqlalchemy.DateTime)  
    # Armazena a data e hora da consulta.

    id_diagnostico = sqlalchemy.Column(sqlalchemy.ForeignKey("Diagnosticos.id_diagnostico"))  
    # Chave estrangeira que referencia o diagnóstico relacionado à consulta.

    prescricao = sqlalchemy.Column(sqlalchemy.Text())  
    # Campo para armazenar a prescrição médica detalhada (campo de texto livre).

    tipo_consulta = sqlalchemy.Column(sqlalchemy.String(100))  
    # Campo para indicar o tipo da consulta (ex: clínica geral, pediatria, etc.).

    id_prontuario = sqlalchemy.Column(sqlalchemy.ForeignKey("Prontuarios.id_prontuario"))  
    # Chave estrangeira para associar a consulta a um prontuário específico.

    id_exame = sqlalchemy.Column(sqlalchemy.ForeignKey("Exames.id_exame"))  
    # Chave estrangeira para associar a consulta a um exame solicitado ou realizado.

    id_faturamento_hospitalar = sqlalchemy.Column(sqlalchemy.ForeignKey("Despesas_Hospitalares.id_despesa_hospitalar"))  
    # Chave estrangeira que liga a consulta ao seu faturamento ou despesa hospitalar correspondente.
