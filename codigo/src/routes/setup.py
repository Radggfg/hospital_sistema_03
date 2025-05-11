# Importa todos os blueprints organizados por módulo
from src.routes.paciente import pacientes, prontuarios
from src.routes.recebimentos_pacientes import recebimento_paciente
from src.routes.profissional import profissional, profissional_leito
from src.routes.administracao import administracao
from src.routes.procedimentos import procedimento, tipo_procedimento
from src.routes.medicamentos import medicamento
from src.routes.leitos import leito
from src.routes.justificativas_ausencias import justificativa_ausencia
from src.routes.fornecedores import fornecedor
from src.routes.estoque_hospitalar import estoque
from src.routes.escalas_trabalhistas import escala_trabalhista, fluxo_horario
from src.routes.equipamentos import equipamento
from src.routes.diagnosticos import diagnostico
from src.routes.consultas import consulta
from src.routes.administracao import administracao  # <-- Redundante, já foi importado acima
from src.routes.exames import exame
from src.routes.tipos_pagamentos import pagamento, tipo_pagamento
from src.routes.profissional import especialidade  # <-- Pode causar conflito com a importação anterior


# Função que registra todos os blueprints no app Flask
def setup_rotas(app):

    # Registra cada módulo no aplicativo principal
    app.register_blueprint(pacientes)
    app.register_blueprint(recebimento_paciente)
    app.register_blueprint(prontuarios)
    app.register_blueprint(profissional)
    app.register_blueprint(profissional_leito)
    app.register_blueprint(administracao)  # <-- aparece duas vezes nas importações, pode ser removido lá de cima
    app.register_blueprint(exame)
    app.register_blueprint(procedimento) 
    app.register_blueprint(tipo_procedimento)
    app.register_blueprint(especialidade)  # <-- nome genérico, cuidado para não conflitar com variáveis ou módulos
    app.register_blueprint(medicamento)
    app.register_blueprint(leito)
    app.register_blueprint(justificativa_ausencia)
    app.register_blueprint(fornecedor)
    app.register_blueprint(estoque)
    app.register_blueprint(escala_trabalhista)
    app.register_blueprint(fluxo_horario)
    app.register_blueprint(equipamento)
    app.register_blueprint(diagnostico)
    app.register_blueprint(consulta)
    app.register_blueprint(pagamento)
    app.register_blueprint(tipo_pagamento)



