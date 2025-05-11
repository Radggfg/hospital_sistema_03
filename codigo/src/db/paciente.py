import sqlalchemy  # Importa o módulo principal do SQLAlchemy.
from sqlalchemy import orm, Enum  # Importa funcionalidades ORM e tipo Enum.

from . import Base  # Importa a base declarativa para os modelos ORM.

# -------------------- MODELO PACIENTE --------------------

class Paciente(Base):
    __tablename__ = "Pacientes"  # Nome da tabela no banco.

    cpf = sqlalchemy.Column(sqlalchemy.String(15), primary_key=True)
    # CPF do paciente – chave primária.

    nome = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome completo do paciente.

    nome_convenio = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome do convênio/plano de saúde.

    num_convenio = sqlalchemy.Column(sqlalchemy.String(100))
    # Número do convênio.

    telefone = sqlalchemy.Column(sqlalchemy.String(100))
    # Telefone de contato principal.

    telefone_contato = sqlalchemy.Column(sqlalchemy.String(100))
    # Telefone de emergência ou contato alternativo.

    endereco = sqlalchemy.Column(sqlalchemy.String(100))
    # Endereço residencial.

    email = sqlalchemy.Column(sqlalchemy.String(100))
    # E-mail do paciente.

    data_nascimento = sqlalchemy.Column(sqlalchemy.Date)
    # Data de nascimento.

    profissao = sqlalchemy.Column(sqlalchemy.String(100))
    # Profissão atual.

    estado_civil = sqlalchemy.Column(sqlalchemy.Enum("solteiro", "casado", "divorciado", "viúvo"))
    # Estado civil do paciente como Enum.

    responsavel = sqlalchemy.Column(sqlalchemy.String(100))
    # Nome do responsável (caso de menores ou pacientes dependentes).


# -------------------- MODELO PACIENTE_MEDICAMENTO --------------------

class Paciente_Medicamento(Base):
    __tablename__ = "Paciente_Medicamento"

    id_paciente_medicamento = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador da prescrição.

    id_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Pacientes.cpf"))
    # FK para paciente.

    id_medicamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Medicamentos.id_medicamento"))
    # FK para medicamento.

    dosagem = sqlalchemy.Column(sqlalchemy.String(50))
    # Dosagem do medicamento (ex: 500mg).

    frequencia = sqlalchemy.Column(sqlalchemy.Enum(
        "Diário", "Semanal", "Mensal", "A cada 8h", "A cada 12h", "A cada 24h"
    ))
    # Frequência da medicação.

    duracao = sqlalchemy.Column(sqlalchemy.INT)
    # Duração do tratamento (dias).

    data_precisao = sqlalchemy.Column(sqlalchemy.Date)
    # Data de início ou previsão de tratamento.

    status = sqlalchemy.Column(sqlalchemy.Enum("Ativo", "Concluído", "Interrompido"))
    # Situação da prescrição.

    observacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Observações adicionais.

    id_profissional_medicamento = sqlalchemy.Column(sqlalchemy.String(100))
    # Identificador do profissional que prescreveu.
    # Sugestão: considerar FK para Profissionais.cpf.


# -------------------- MODELO PACIENTE_LEITO --------------------

class Paciente_Leito(Base):
    __tablename__ = "Paciente_Leito"

    id_paciente_leito = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador da internação.

    id_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Pacientes.cpf"))
    # FK para o paciente internado.

    id_leito = sqlalchemy.Column(sqlalchemy.ForeignKey("Leitos.id_leito"))
    # FK para o leito ocupado.

    data_internacao = sqlalchemy.Column(sqlalchemy.DateTime)
    # Data/hora de entrada no hospital.

    data_alta = sqlalchemy.Column(sqlalchemy.DateTime)
    # Data/hora de alta médica.

    status = sqlalchemy.Column(sqlalchemy.Enum("Internado", "Alta", "Transferido", "Óbito"))
    # Status atual da internação.

    observacoes = sqlalchemy.Column(sqlalchemy.Text())
    # Comentários adicionais sobre o caso clínico.


# -------------------- MODELO RECEBIMENTOS_PACIENTES --------------------

class Recebimento_Paciente(Base):
    __tablename__ = "Recebimentos_Pacientes"

    id_recebimento_paciente = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    # Identificador do recebimento financeiro.

    id_paciente = sqlalchemy.Column(sqlalchemy.ForeignKey("Pacientes.cpf"))
    # FK para o paciente (⚠️ corrigido para CPF).

    id_consulta = sqlalchemy.Column(sqlalchemy.ForeignKey("Consultas.id_consulta"))
    # FK para consulta realizada.

    id_procedimento = sqlalchemy.Column(sqlalchemy.ForeignKey("Procedimentos.id_procedimento"))
    # FK para procedimento executado.

    id_exame = sqlalchemy.Column(sqlalchemy.ForeignKey("Exames.id_exame"))
    # FK para exame.

    id_medicamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Medicamentos.id_medicamento"))
    # FK para medicamento utilizado/fornecido.

    valor_total = sqlalchemy.Column(sqlalchemy.DECIMAL())
    # Valor total cobrado/recebido.

    id_pagamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Pagamentos.id_pagamento"))
    # FK para a transação de pagamento.

    id_tipo_pagamento = sqlalchemy.Column(sqlalchemy.ForeignKey("Tipos_Pagamentos.id_tipo_pagamento"))
    # FK para tipo de pagamento (ex: cartão, convênio, pix, boleto).

    data_recebimento = sqlalchemy.Column(sqlalchemy.DateTime())
    # Data/hora do recebimento.
