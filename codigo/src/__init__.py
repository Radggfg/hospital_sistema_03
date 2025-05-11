# Importa a classe Flask do pacote flask para criar a aplicação
from flask import Flask

# Instancia a aplicação Flask
app = Flask(__name__)

# Credenciais e informações do banco de dados hospedado na AWS RDS
LOGIN = "rafael.marostica"
SENHA = "Qi7^,xpV?k6Y0.a1"  
HOST = "rafael-marostica.cjaewoikmvie.sa-east-1.rds.amazonaws.com"
DATABASE = "hospital_db"

# Configuração da URI de conexão com banco de dados MySQL utilizando PyMySQL como driver
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{LOGIN}:{SENHA}@{HOST}/{DATABASE}'

# Importa o módulo interno que contém as definições do banco (modelos e configurações)
from . import db

# Importa a classe datetime.date caso queira utilizar para datas no futuro
from datetime import date

# Importa o modelo Paciente que será usado para realizar consultas
from .db.paciente import Paciente

# Inicializa o SQLAlchemy com a aplicação Flask configurada
from flask_sqlalchemy import SQLAlchemy
banco = SQLAlchemy(app)

# Define a rota raiz do sistema
@app.route("/")
def index():
    # Garante que transações anteriores estejam encerradas
    banco.session.commit()

    # Realiza uma query para buscar todos os registros da tabela de pacientes
    query = banco.session.query(Paciente)

    # Retorna diretamente o objeto de query (em ambiente real, o ideal seria converter para JSON)
    return query
