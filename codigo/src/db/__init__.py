from sqlalchemy import MetaData  # Importa a classe MetaData, que representa o conjunto de metadados (esquema) do banco de dados.

from sqlalchemy import orm  # Importa o módulo ORM, que permite mapear classes Python para tabelas do banco de dados.

metadata_obj = MetaData()  # Cria uma instância de MetaData que armazenará informações sobre as tabelas e relacionamentos definidos.

Base = orm.declarative_base(metadata=metadata_obj)  # Cria a classe base para os modelos ORM. Todos os modelos devem herdar dessa classe.
                                                    # O parâmetro 'metadata=metadata_obj' garante que todas as tabelas compartilhem os mesmos metadados.