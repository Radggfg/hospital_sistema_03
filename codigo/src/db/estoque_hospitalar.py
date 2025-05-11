import sqlalchemy  # Importa o módulo principal do SQLAlchemy.

from sqlalchemy import orm, Enum  # Importa o ORM e o tipo Enum (usado para categorias e status).

from . import Base  # Importa a classe base dos modelos (declarative_base).

class Estoque_hospitalar(Base):  # Define o modelo ORM para representar o estoque do hospital.
    __tablename__ = "Estoque_Hospitalar"  # Define o nome da tabela no banco de dados.

    id_estoque = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária do estoque, usada para identificar de forma única cada registro.

    id_produto = sqlalchemy.Column(sqlalchemy.ForeignKey("Medicamentos.id_medicamento"))
    # Chave estrangeira que associa o item de estoque a um produto da tabela 'Medicamentos'.
    # (Sugestão: adaptar para suportar múltiplos tipos de produtos, se necessário.)

    categoria = sqlalchemy.Column(sqlalchemy.Enum(
        'Medicamento', 'Equipamento', 'Material Hospitalar', 'Outros'
    ))
    # Enum que define a categoria do item armazenado no estoque, garantindo padronização.

    quantidade = sqlalchemy.Column(sqlalchemy.INT)
    # Quantidade atual do item no estoque.

    data_entrada = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data e hora em que o item foi registrado ou entrou no estoque.

    data_atualizacao = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data e hora da última atualização do registro de estoque (ex: entrada, baixa, ajuste).

    status = sqlalchemy.Column(sqlalchemy.Enum(
        'Disponível', 'Esgotado', 'Próximo do Vencimento', 'Vencido'
    ))
    # Enum que indica a situação atual do item no estoque.
    # Ajuda no controle logístico e farmacêutico (por exemplo, alerta de validade).
