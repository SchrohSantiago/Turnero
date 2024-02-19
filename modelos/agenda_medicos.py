import csv   # Importacion para leer el CSV
from flask import request
from datetime import datetime
import os
csv_agenda_medicos = "modelos//agenda_medicos.csv"


agenda_medicos = []


def import_csv():
    global agenda_medicos # La declaramos con global para un uso global

    agenda_medicos = []

    with open(csv_agenda_medicos, newline='') as csvfile:  
        reader = csv.DictReader(csvfile) # DictReader permite la lectura de datos por columna
        for row in reader:
            #Convertimos el ID de cadena a entero
            
            agenda_medicos.append(row)


def export_csv():
    with open(csv_agenda_medicos, 'w', newline='') as csvfile:
        fecha_actual = datetime.now().strftime('%Y/%m/%d')

        campo_nombres = ['id_medico', 'dia_numero', 'hora_inicio', 'hora_fin', 'fecha_actualizacion']
        writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)
        writer.writeheader()
        
        for agenda_medic in agenda_medicos:
            agenda_medic['fecha_actualizacion'] = fecha_actual  # Agregamos la fecha actual al CSV
            writer.writerow(agenda_medic)





def obtener_agenda_medicos():
    global agenda_medicos

    ahora = datetime.now()

    if os.path.exists(csv_agenda_medicos):
        import_csv()

        horarios_info = [
            (agenda['id_medico'], agenda['dia_numero'], agenda['hora_inicio'], agenda['hora_fin'])
            for agenda in agenda_medicos
        ]

        # ordenamos por dia y hora
        horarios_info.sort(key=lambda x: (x[0], x[1], x[2]))

        # filtramos los NO vencidos
        horarios_disponibles = [
            info for info in horarios_info 
            if (
                (datetime.strptime(info[3], '%H:%M').time() > ahora.time() and int(info[1]) == ahora.weekday())
                or (int(info[1]) > ahora.weekday())
            )
        ]

        return horarios_disponibles

    return None




def agregar_agenda_medico(data):
    import_csv()
    global agenda_medicos

    agenda_medicos.append({
        'id_medico': data['id_medico'],
        'dia_numero': data['dia_numero'],
        'hora_inicio': data['hora_inicio'],
        'hora_fin': data['hora_fin'],
        })

    export_csv()

    return agenda_medicos

        

def formato_hora(hora): 
    try:
        datetime.strptime(hora, '%H:%M')
        return True
    except ValueError:
        return False
    
def validar_turno_existente(id_medico, dia_numero):
    import_csv()
    global agenda_medicos

   

    # Filtrar la agenda del médico y día específico
    for agenda in agenda_medicos:
        if agenda['id_medico'] == str(id_medico) and agenda['dia_numero'] == dia_numero:
            return False

    return True


def modificar_horarios_agenda(id,data):
    import_csv()
    global agenda_medicos   
    
    
    for agenda in agenda_medicos:
        if agenda['id_medico'] == str(id) and agenda['dia_numero'] == data['dia_numero']:
            agenda['hora_inicio'] = data['hora_inicio']
            agenda['hora_fin'] = data['hora_fin']
      
    export_csv()
    
    return agenda_medicos

        

def desabilitar_agenda_medico(id_medico):
    import_csv()
    global agenda_medicos

    # Filtrar las agendas del médico específico
    agendas_a_eliminar = [agenda for agenda in agenda_medicos if agenda['id_medico'] == str(id_medico)]

    # Eliminar las agendas del médico
    for agenda in agendas_a_eliminar:
        agenda_medicos.remove(agenda)

    export_csv()

    return agenda_medicos


def validar_horario_turno(id_medico, dia_numero, hora_inicio):
    import_csv()
    global agenda_medicos

    # Buscar la agenda del médico y día específico
    for agenda in agenda_medicos:
        if agenda['id_medico'] == id_medico and agenda['dia_numero'] == dia_numero:
    
            hora_inicio_turno = datetime.strptime(hora_inicio, '%H:%M').time()


            # Verificar si las horas del turno están dentro del rango de horas laborales
          
    return True


def validar_intervalo_15_minutos(hora_inicio, hora_fin):
    # Verificar si la diferencia entre la hora de inicio y la hora de fin es un múltiplo de 15 minutos
    diferencia = datetime.combine(datetime.today(), hora_fin) - datetime.combine(datetime.today(), hora_inicio)
    minutos = diferencia.total_seconds() / 60
    return minutos % 15 == 0