from flask import Flask
#Integrantes: Nicolas Clemente y Santiago Schroh

from controladores.ruta_pacientes import pacientes_bp
from controladores.ruta_medicos import medicos_bp
from controladores.ruta_agenda_medicos import agenda_medicos_bp
from controladores.ruta_turnos_medicos import turnos_bp
from modelos.pacientes import crear_pacientes_api
from modelos.medicos import crear_medico_api



app = Flask(__name__) #creamos una instancia de la clase

crear_pacientes_api()
crear_medico_api()


app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(agenda_medicos_bp)    
app.register_blueprint(turnos_bp)

if __name__ == '__main__':
    app.run(debug=True)

