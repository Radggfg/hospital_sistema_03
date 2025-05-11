import sqlalchemy  # Importa o módulo principal do SQLAlchemy.

from sqlalchemy import orm, Enum  # Importa o ORM e o tipo Enum, usado para campos com valores fixos.

from . import Base  # Importa a base do ORM, necessária para declarar a tabela.

class Equipamento(Base):  # Define a classe Equipamento como modelo ORM.
    __tablename__ = "Equipamentos"  # Define o nome da tabela como 'Equipamentos' no banco de dados.

    id_equipamento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária da tabela. Identificador único para cada equipamento.

    descricao = sqlalchemy.Column(sqlalchemy.Text())
    # Campo descritivo do equipamento. Pode conter informações detalhadas sobre a função e uso.

    nome_equipamento = sqlalchemy.Column(sqlalchemy.String(255))
    # Nome do equipamento (ex: "Monitor cardíaco", "Bisturi elétrico").

    categoria = sqlalchemy.Column(sqlalchemy.Enum(
        'DIAGNÓSTICO', 'TERAPÊUTICO', 'CIRÚRGICO', 'LABORATORIAL', 'HOSPITALAR_GERAL'
    ))
    # Enum que define a categoria funcional do equipamento.
    # Permite classificar o equipamento para controle e organização.

    custo_base = sqlalchemy.Column(sqlalchemy.DECIMAL())
    # Valor original de aquisição do equipamento.

    custo_manutencao = sqlalchemy.Column(sqlalchemy.DECIMAL())
    # Custo estimado ou real de manutenção do equipamento ao longo do tempo.

    setor = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome do setor onde o equipamento está alocado (ex: UTI, bloco cirúrgico).

    fabricante = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome da empresa ou marca que fabrica o equipamento.

    modelo = sqlalchemy.Column(sqlalchemy.String(100))
    # Modelo específico do equipamento (identificação técnica).

    numero_serie = sqlalchemy.Column(sqlalchemy.String(50))
    # Número de série do equipamento para controle patrimonial.

    vida_util = sqlalchemy.Column(sqlalchemy.INT)
    # Tempo estimado de uso (em anos, meses etc.) até que o equipamento se torne obsoleto ou inutilizável.

    estado_atual = sqlalchemy.Column(sqlalchemy.Enum(
        'NOVO', 'EM_USO', 'EM_MANUTENÇÃO', 'INATIVO', 'DESCARTADO'
    ))
    # Enum que representa o status atual do equipamento.
    # Útil para manutenção preventiva, controle de inventário, etc.

    data_aquisicao = sqlalchemy.Column(sqlalchemy.DateTime)
    # Data em que o equipamento foi comprado ou chegou ao hospital.

    fornecedor = sqlalchemy.Column(sqlalchemy.ForeignKey("Fornecedores.cnpj"))
    # Chave estrangeira que vincula o equipamento a um fornecedor.

    despesa_hospitalar = sqlalchemy.Column(sqlalchemy.ForeignKey("Despesas_Hospitalares.id_despesa_hospitalar"))
    # Chave estrangeira que relaciona esse equipamento a uma despesa hospitalar específica.

