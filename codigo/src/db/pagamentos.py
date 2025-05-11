import sqlalchemy  # Importa o módulo principal do SQLAlchemy.
from sqlalchemy import orm, Enum  # Importa recursos de ORM e Enum (caso necessário para status ou tipo).
from . import Base  # Importa a classe base declarativa para definição dos modelos ORM.

# ---------------------------- MODELO PAGAMENTO ----------------------------

class Pagamento(Base):
    __tablename__ = "Pagamentos"  # Nome da tabela no banco de dados.

    id_pagamento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único de cada pagamento. Chave primária da tabela.

    tipo_pagamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Tipos_Pagamentos.id_tipo_pagamento"))
    # Chave estrangeira referenciando o tipo de pagamento utilizado (ex: PIX, cartão).

    comprovante_pagamento = sqlalchemy.Column(sqlalchemy.String(255))
    # Nome do arquivo, código ou caminho para o comprovante do pagamento.

    status_pagamento = sqlalchemy.Column(sqlalchemy.String(255))
    # Status do pagamento (ex: "pendente", "realizado", "cancelado").

    data_pagamento = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data e hora em que o pagamento foi efetuado ou registrado.

    num_parcelas = sqlalchemy.Column(sqlalchemy.INT)
    # Número de parcelas, se o pagamento foi parcelado.

    valor_pago = sqlalchemy.Column(sqlalchemy.DECIMAL())
    # Valor total pago na transação.

    fluxo_pagamento = sqlalchemy.Column(sqlalchemy.String(255))
    # Descrição do fluxo de pagamento (ex: "à vista", "convênio", "cartão corporativo").

    id_recebimento_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Recebimentos_Pacientes.id_recebimento_paciente"))
    # Chave estrangeira para o recebimento relacionado ao paciente (entrada de valor).

    id_despesa_hospitalar = sqlalchemy.Column(sqlalchemy.ForeignKey("Despesas_Hospitalares.id_despesa_hospitalar"))
    # Chave estrangeira para a despesa hospitalar associada (saída de valor).


# ------------------------ MODELO TIPO DE PAGAMENTO ------------------------

class Tipo_Pagamento(Base):
    __tablename__ = "Tipos_Pagamentos"  # Nome da tabela no banco de dados.

    id_tipo_pagamento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único do tipo de pagamento. Chave primária.

    nome_tipo_pagamento = sqlalchemy.Column(sqlalchemy.String(255))
    # Nome descritivo do tipo de pagamento (ex: "Cartão de Crédito", "PIX", "Convênio").
