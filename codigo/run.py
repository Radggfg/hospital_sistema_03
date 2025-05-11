# Importa a instância do app Flask definida em src/__init__.py
from src import app

# Importa a função que registra todas as rotas definidas nos Blueprints
from src.routes.setup import setup_rotas

# Registra todas as rotas do sistema usando a função setup_rotas
setup_rotas(app)

# Inicia o servidor Flask com modo debug ativado (útil em desenvolvimento)
app.run(debug=True)
