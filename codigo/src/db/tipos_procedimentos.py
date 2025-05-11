import sqlalchemy  # Importa o módulo principal do SQLAlchemy.
from sqlalchemy import orm, Enum  # Importa recursos ORM e tipo enumerado (Enum).
from . import Base  # Importa a base declarativa usada para definição dos modelos ORM.

# ------------------------------ MODELO TIPO DE PROCEDIMENTO ------------------------------

class Tipo_Procedimento(Base):
    __tablename__ = "Tipos_procedimentos"  # Nome da tabela no banco de dados.

    id_tipo_procedimento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único do tipo de procedimento – chave primária.

    descricao = sqlalchemy.Column(sqlalchemy.Text())
    # Descrição detalhada do procedimento (ex: finalidade, contexto de uso, metodologia).

    nome_procedimento = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome do procedimento (ex: “Curativo Simples”, “Endoscopia”, “Cirurgia de hérnia”).

    categoria = sqlalchemy.Column(sqlalchemy.String(100))
    # Categoria geral do procedimento (ex: “Ambulatorial”, “Cirúrgico”, “Diagnóstico”).

    custo_base = sqlalchemy.Column(sqlalchemy.DECIMAL())
    # Custo estimado ou padrão do procedimento, usado para orçamento e controle de despesas.

    risco = sqlalchemy.Column(sqlalchemy.Enum('BAIXO', 'MODERADO', 'ALTO', 'CRÍTICO', 'NENHUM'))
    # Grau de risco envolvido no procedimento, com valores controlados por Enum.

    equipamentos_necessarios = sqlalchemy.Column(sqlalchemy.Text())
    # Lista textual ou descritiva dos equipamentos que devem estar disponíveis para execução.
