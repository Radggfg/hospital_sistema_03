import sqlalchemy  # Importa o módulo base do SQLAlchemy, com tipos de dados e funcionalidades para definição de colunas.

from sqlalchemy import orm, Enum  # Importa recursos do ORM e o tipo Enum (ainda que não utilizado neste trecho específico).

from . import Base  # Importa a classe base dos modelos, que define o mapeamento ORM para o banco de dados.

class Despesa_Hospitalar(Base):  # Define o modelo Despesa_Hospitalar como uma tabela no banco.
    __tablename__ = "Despesas_Hospitalares"  # Nome da tabela que será criada no banco de dados.

    id_despesa_hospitalar = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária da despesa hospitalar, identificador único de cada registro.

    id_medicamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Medicamentos.id_medicamento"))
    # Chave estrangeira que vincula a despesa a um medicamento específico.

    id_equipamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Equipamentos.id_equipamento"))
    # Chave estrangeira que vincula a despesa a um equipamento utilizado ou comprado.

    id_salario_profissional = sqlalchemy.Column(sqlalchemy.INT)
    # Campo que pode armazenar o identificador de uma despesa relacionada ao salário de um profissional.
    # (Sugestão: considerar torná-lo ForeignKey para uma tabela de salários, se existir.)

    valor_total = sqlalchemy.Column(sqlalchemy.DECIMAL())
    # Valor total da despesa hospitalar. Usa tipo DECIMAL para maior precisão em cálculos financeiros.

    id_exame = sqlalchemy.Column(sqlalchemy.ForeignKey("Exames.id_exame"))
    # Chave estrangeira que associa a despesa a um exame realizado.

    id_pagamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Pagamentos.id_pagamento"))
    # Chave estrangeira que liga a despesa a um pagamento específico.

    id_tipo_pagamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Tipos_Pagamentos.id_tipo_pagamento"))
    # Chave estrangeira que identifica o tipo de pagamento (ex: cartão, boleto, convênio).

    id_leito = sqlalchemy.Column(sqlalchemy.ForeignKey("Leitos.id_leito"))
    # Chave estrangeira que associa a despesa ao uso de um leito hospitalar.

    id_procedimento = sqlalchemy.Column(sqlalchemy.ForeignKey("Procedimentos.id_procedimento"))
    # Chave estrangeira que vincula a despesa a um procedimento médico ou cirúrgico.

    id_consulta = sqlalchemy.Column(sqlalchemy.INT)
    # Identificador de uma consulta associada à despesa. (Sugestão: considerar uso de ForeignKey para `Consultas.id_consulta`.)

    id_fornecedor = sqlalchemy.Column(sqlalchemy.ForeignKey("Fornecedores.cnpj"))
    # Chave estrangeira que associa a despesa a um fornecedor (de medicamento, equipamento, etc.).

    data_despesa = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data em que a despesa foi realizada ou registrada no sistema.


