from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://schroh:1545492-sS@localhost:3306/turnero_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Registrar blueprints después de inicializar la aplicación y la base de datos
from controladores.ruta_pacientes import pacientes_bp
from controladores.ruta_medicos import medicos_bp
from controladores.ruta_agenda_medicos import agenda_medicos_bp
from controladores.ruta_turnos_medicos import turnos_bp

app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(agenda_medicos_bp)
app.register_blueprint(turnos_bp)

if __name__ == '__main__':
    app.run(debug=True)
