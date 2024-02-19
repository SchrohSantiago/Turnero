import csv   # Importacion para leer el CSV
import os # 
from datetime import datetime
csv_turnos = "modelos//turnos.csv"

turnos = []

def import_csv():
    global turnos # La declaramos con global para un uso global
    
    turnos = []

    with open(csv_turnos, newline='') as csvfile:  
        reader = csv.DictReader(csvfile) # DictReader permite la lectura de datos por columna
        for row in reader:
            #Convertimos el ID de cadena a entero
            turnos.append(row)


def export_csv():
     with open(csv_turnos, 'w', newline='') as csvfile:
        campo_nombres = ['id_medico','id_paciente','hora_turno','fecha_solicitud']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        for turno in turnos:
            writer.writerow(turno)

def obtener_turnos_medicos(id_search):
    import_csv()
    
    turnos_medico = []

    if os.path.exists(csv_turnos):
        for turno in turnos: 
            if turno['id_medico'] == str(id_search):  # Asegúrate de comparar con una cadena si 'id_medico' es una cadena en tus datos
                turnos_medico.append(turno)
    
    return turnos_medico 


def turno_eliminado(id_medico, id_paciente): # La consigna dice por ID, pero voy a utilizar los dos ID para que la eliminacion del turno sea mas certera
    import_csv()
    print(turnos)

    for i in turnos:
        if i['id_medico'] == str(id_medico) and i['id_paciente'] == str(id_paciente):
            turnos.remove(i)
            export_csv()
            return turnos
    
def turno_agregado(data):
    import_csv()
    
    turno = {'id_medico': data['id_medico'], 'id_paciente': data['id_paciente'], 'hora_turno': data['hora_turno'], 'fecha_solicitud': data['fecha_solicitud']}
    turnos.append(turno)
    export_csv()
    return turnos

def validar_fecha(fecha): 
    try:
        fecha_ingresada = datetime.strptime(fecha, '%Y/%m/%d').date()
        fecha_actual = datetime.now().date()
        
        # Verificar si la fecha es el día actual o posterior al día actual
        if fecha_ingresada >= fecha_actual:
            # Calcular la diferencia en días entre la fecha ingresada y la actual
            diferencia_dias = (fecha_ingresada - fecha_actual).days

            # Verificar si la diferencia es menor o igual a 30 días
            if 0 <= diferencia_dias <= 30:
                return True
            else:
                return False
        else:
            return False
    except ValueError:
        # Capturar errores si el formato de la fecha no es válido
        return False

def verificar_turno_creado(medico, turn, fecha):
    import_csv()

    print(medico, turn, fecha)

    for turno in turnos:
           
        if turno['id_medico'] == medico and turno['hora_turno'] == turn and  turno['fecha_solicitud'] == fecha:
            return False

    return True

def turnos_pendientes():
    import_csv()

    turnos_pendientes = []

    # Obtener la fecha y hora actuales
    ahora = datetime.now()

    for turno in turnos:
        # Convertir la fecha y hora del turno a objetos datetime
        fecha_turno = datetime.strptime(turno['fecha_solicitud'] + ' ' + turno['hora_turno'], '%Y/%m/%d %H:%M')
        print(fecha_turno)
        # Verificar si el turno está pendiente
        if fecha_turno > ahora:
            turnos_pendientes.append(turno)
    return turnos_pendientes
