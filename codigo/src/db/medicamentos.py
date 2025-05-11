import sqlalchemy  # Importa o módulo principal do SQLAlchemy, necessário para definição de colunas e tipos.

from sqlalchemy import orm, Enum  # Importa funcionalidades do ORM e o tipo Enum, usado para valores fixos.

from . import Base  # Importa a classe base de todos os modelos ORM do projeto.

class Medicamento(Base):  # Define o modelo Medicamento, que representa os remédios disponíveis no hospital.
    __tablename__ = "Medicamentos"  # Nome da tabela no banco de dados.

    id_medicamento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único do medicamento — chave primária da tabela.

    nome_medicamento = sqlalchemy.Column(sqlalchemy.String(255))
    # Nome comercial do medicamento (ex: Dipirona, Paracetamol).

    principio_ativo = sqlalchemy.Column(sqlalchemy.String(255))
    # Componente químico responsável pela ação terapêutica do medicamento.

    dosagem = sqlalchemy.Column(sqlalchemy.String(50))
    # Indicação da dose (ex: 500mg, 1g, 5ml a cada 8h).

    restricao = sqlalchemy.Column(sqlalchemy.Text())
    # Restrições de uso (ex: "não indicado para menores de 12 anos").

    bula = sqlalchemy.Column(sqlalchemy.Text())
    # Texto completo da bula ou resumo das instruções do fabricante.

    indicacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Situações ou doenças em que o medicamento deve ser usado.

    contra_indicacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Situações em que o medicamento **não** deve ser utilizado (ex: alergias, gravidez).

    lote = sqlalchemy.Column(sqlalchemy.String(50))
    # Código do lote do medicamento, importante para rastreabilidade e controle de qualidade.

    data_validade = sqlalchemy.Column(sqlalchemy.Date())
    # Data de vencimento do medicamento.

    fabricante = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome do laboratório fabricante.

    preco_unitario = sqlalchemy.Column(sqlalchemy.DECIMAL())
    # Valor de custo por unidade do medicamento, usado para controle financeiro e faturamento.

    tarja = sqlalchemy.Column(sqlalchemy.Enum('SEM_TARJA','AMARELA','VERMELHA','PRETA'))
    # Enum que define a tarja do medicamento, relacionada à sua classificação de controle:
    # - SEM_TARJA: uso livre
    # - AMARELA: controle leve
    # - VERMELHA: controlado
    # - PRETA: controlado com receita especial

    id_fornecedor = sqlalchemy.Column(sqlalchemy.ForeignKey("Fornecedores.cnpj"))
    # Chave estrangeira que relaciona o medicamento a um fornecedor cadastrado.



