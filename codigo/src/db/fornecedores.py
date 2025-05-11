import sqlalchemy  # Importa o módulo principal do SQLAlchemy.

from sqlalchemy import orm, Enum  # Importa ferramentas do ORM e o tipo Enum (embora não usado aqui).

from sqlalchemy.sql import func  # Importa funções SQL, como 'now()', para uso em campos com valores padrão.

from . import Base  # Importa a classe base de todos os modelos ORM (declarative_base).

class Fornecedor(Base):  # Define a classe Fornecedor como um modelo mapeado para a tabela de fornecedores.
    __tablename__ = "Fornecedores"  # Nome da tabela no banco de dados.

    nome_fornecedor = sqlalchemy.Column(sqlalchemy.String(255))
    # Nome completo ou razão social do fornecedor.

    cnpj = sqlalchemy.Column(sqlalchemy.String(18), primary_key=True)
    # CNPJ (Cadastro Nacional de Pessoa Jurídica), usado como identificador único do fornecedor.
    # É a chave primária da tabela.

    telefone = sqlalchemy.Column(sqlalchemy.String(20))
    # Número de telefone para contato com o fornecedor.

    email = sqlalchemy.Column(sqlalchemy.String(255))
    # Endereço de e-mail do fornecedor.

    endereco = sqlalchemy.Column(sqlalchemy.Text())
    # Endereço físico completo do fornecedor (rua, número, bairro, etc.).

    cidade = sqlalchemy.Column(sqlalchemy.String(100))
    # Cidade onde o fornecedor está localizado.

    estado = sqlalchemy.Column(sqlalchemy.String(2))
    # Unidade federativa (UF) do fornecedor, geralmente representada por duas letras (ex: "SP", "RJ").

    tipo_fornecedor = sqlalchemy.Column(sqlalchemy.String(100))
    # Tipo ou categoria do fornecedor (ex: "medicamentos", "equipamentos", "serviços", etc.).

    data_cadastro = sqlalchemy.Column(sqlalchemy.DateTime(), default=func.now())
    # Data e hora em que o fornecedor foi cadastrado no sistema.
    # Usa `func.now()` para registrar automaticamente o momento do cadastro.
