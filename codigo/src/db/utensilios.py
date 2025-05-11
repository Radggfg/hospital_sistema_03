import sqlalchemy  # Importa o SQLAlchemy para definição das colunas e tipos.
from sqlalchemy import orm, Enum  # ORM para mapeamento e suporte a campos do tipo Enum.
from . import Base  # Importa a classe base usada para declarar os modelos ORM.

# ------------------------------ MODELO MEDICAMENTO ------------------------------

class Medicamento(Base):
    __tablename__ = "Medicamentos"  # Nome da tabela no banco de dados.

    id_medicamento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador único do medicamento – chave primária.

    nome_medicamento = sqlalchemy.Column(sqlalchemy.String(255))
    # Nome comercial do medicamento (ex: Dipirona, Paracetamol).

    principio_ativo = sqlalchemy.Column(sqlalchemy.String(255))
    # Substância responsável pelo efeito terapêutico (ex: Ibuprofeno, Amoxicilina).

    dosagem = sqlalchemy.Column(sqlalchemy.String(50))
    # Dosagem recomendada por unidade (ex: 500mg, 1g, 20 gotas).

    restricao = sqlalchemy.Column(sqlalchemy.Text())
    # Restrições de uso (ex: contraindicado para menores de 12 anos, gestantes, etc.).

    bula = sqlalchemy.Column(sqlalchemy.Text())
    # Conteúdo integral ou resumido da bula (instruções do fabricante).

    indicacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Condições ou doenças para as quais o medicamento é recomendado.

    contraindicacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Situações ou condições em que o medicamento **não** deve ser utilizado.

    lote = sqlalchemy.Column(sqlalchemy.Date)
    # ⚠️ OBSERVAÇÃO: este campo parece estar incorreto — lote geralmente é um código (string), não uma data.
    # Sugestão: `sqlalchemy.String(50)` seria mais apropriado.

    fabricante = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome do laboratório ou empresa que fabrica o medicamento.

    preco_unitario = sqlalchemy.Column(sqlalchemy.Float)
    # Preço por unidade, usado para controle de estoque e custos.

    tarja = sqlalchemy.Column(sqlalchemy.Enum('SEM_TARJA', 'AMARELA', 'VERMELHA', 'PRETA'))
    # Tarja do medicamento:
    # - SEM_TARJA: venda livre
    # - AMARELA: psicotrópicos leves
    # - VERMELHA: controlado
    # - PRETA: controlado de uso restrito

    id_fornecedor = sqlalchemy.Column(sqlalchemy.ForeignKey("Fornecedores.cnpj"))
    # Chave estrangeira que relaciona o medicamento a um fornecedor cadastrado.
