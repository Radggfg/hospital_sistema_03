import sqlalchemy  # Importa o módulo principal do SQLAlchemy.

from . import Base  # Importa a classe base usada como superclasse para todos os modelos ORM.

import enum  # <- enum do Python, para criar classes Enum

import sqlalchemy
from sqlalchemy import Column, Enum  # <- Column e Enum do SQLAlchemy, para modelar campos no banco


# Define a classe Exame, que representa exames solicitados ou realizados no hospital
class Exame(Base):
    __tablename__ = "Exames"  # Nome da tabela no banco de dados

    # Enum que define os possíveis status operacionais do exame
    class StatusExameEnum(str, enum.Enum):
        pendente = "pendente"                    # Exame solicitado, mas não iniciado
        agendado = "agendado"                    # Data e hora marcadas
        em_andamento = "em_andamento"            # Exame está sendo realizado
        finalizado = "finalizado"                # Exame concluído
        laudo_pronto = "laudo_pronto"            # Resultado/laudo está disponível
        cancelado = "cancelado"                  # Exame cancelado
        rejeitado = "rejeitado"                  # Exame invalidado
        repetir_exame = "repetir_exame"          # Repetição do exame solicitada

    # Enum que define os estados do resultado do exame
    class ResultadoExameEnum(str, enum.Enum):
        pendente = "pendente"                          # Sem resultado ainda
        agendado = "agendado"                          # Data de entrega do resultado marcada
        em_andamento = "em_andamento"                  # Resultado está sendo produzido
        realizado = "realizado"                        # Exame foi executado com sucesso
        laudo_disponivel = "laudo_disponivel"          # Resultado está disponível
        cancelado = "cancelado"                        # Resultado cancelado
        rejeitado = "rejeitado"                        # Resultado rejeitado por falha
        repeticao_solicitada = "repeticao_solicitada"  # Novo exame necessário

    tipo_exame = sqlalchemy.Column(sqlalchemy.String(100))
    # Tipo do exame (ex: "Hemograma", "Raio-X", "Tomografia")

    descricao_exame = sqlalchemy.Column(sqlalchemy.String(100))
    # Descrição complementar do exame, se necessário

    data_solicitacao = sqlalchemy.Column(sqlalchemy.DateTime)
    # Data e hora em que o exame foi solicitado pelo profissional de saúde

    data_realizacao = sqlalchemy.Column(sqlalchemy.DateTime)
    # Data e hora em que o exame foi realizado (se aplicável)

    laudo_medico = sqlalchemy.Column(sqlalchemy.String(100))
    # Caminho do arquivo ou nome do laudo gerado, ou uma descrição resumida

    status_exame = sqlalchemy.Column(sqlalchemy.Enum(StatusExameEnum))
    # Status atual do exame, com valores definidos no Enum

    resultado_exame = sqlalchemy.Column(sqlalchemy.Enum(ResultadoExameEnum))
    # Estado do resultado/laudo do exame

    observacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Campo livre para anotações adicionais do profissional de saúde

    assinatura_profissional = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome ou identificador da assinatura do profissional responsável

    id_exame = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Chave primária da tabela, identificador único de cada exame

    id_procedimento = sqlalchemy.Column(sqlalchemy.ForeignKey("Procedimentos.id_procedimento"))
    # Chave estrangeira para a tabela de Procedimentos (relaciona com o procedimento médico)

    id_prontuario = sqlalchemy.Column(sqlalchemy.ForeignKey("Prontuarios.id_prontuario"))
    # Chave estrangeira para a tabela de Prontuários (relaciona com o prontuário do paciente)

    id_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Pacientes.cpf"))
    # Chave estrangeira para a tabela de Pacientes (identificado pelo CPF)

    id_profissional = sqlalchemy.Column(sqlalchemy.ForeignKey("Profissionais.cpf"))
    # Chave estrangeira para a tabela de Profissionais (identificado pelo CPF do médico ou técnico)

