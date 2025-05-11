import sqlalchemy  # Importa o módulo principal do SQLAlchemy, incluindo tipos e utilitários para definição de colunas.

from sqlalchemy import orm, Enum  # Importa recursos do ORM e o tipo Enum para colunas com valores fixos.

from . import Base  # Importa a classe base que serve de ponto de partida para todos os modelos (declarative_base).

class Departamento(Base):  # Define a classe Departamento como um modelo ORM.
    __tablename__ = "Departamentos"  # Define o nome da tabela no banco de dados como 'Departamentos'.

    id_departamento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária da tabela, identificador único de cada departamento.

    nome = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome do departamento (ex: Cardiologia, Administrativo, RH).

    sigla = sqlalchemy.Column(sqlalchemy.String(100))
    # Sigla ou abreviação usada internamente para identificar o departamento.

    descricao = sqlalchemy.Column(sqlalchemy.TEXT)
    # Descrição detalhada do departamento e suas funções.

    andar_localizacao = sqlalchemy.Column(sqlalchemy.String(100))
    # Informa o andar ou local físico onde o departamento está situado.

    ramal_telefone = sqlalchemy.Column(sqlalchemy.String(100))
    # Número do ramal telefônico do departamento.

    email = sqlalchemy.Column(sqlalchemy.String(100))
    # E-mail de contato do departamento.

    id_responsavel = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))
    # Chave estrangeira que referencia o CPF do profissional responsável pelo departamento.

    status = sqlalchemy.Column(sqlalchemy.Enum(
        'ativo',
        'em manutenção',
        'aguardando aprovação',
        'desativado temporariamente',
        'desativado permanentemente'
    ))
    # Enum para indicar o status atual do departamento com valores pré-definidos.

    data_cricao = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data em que o departamento foi criado (campo opcional de controle temporal).

    data_atualizacao = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data da última atualização das informações do departamento.
