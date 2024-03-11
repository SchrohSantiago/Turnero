from flask import Blueprint, jsonify, request
from modelos.turnos import obtener_turnos_medicos, turno_eliminado, validar_fecha, agregar_turno, verificar_turno_creado, turnos_pendientes
from modelos.medicos import obtener_medico_id, verificar_habilitacion_medico
from modelos.pacientes import obtener_paciente_id
from modelos.agenda_medicos import formato_hora

turnos_bp = Blueprint('turnos_bp', __name__)

@turnos_bp.route('/turnos/<int:id_search>', methods=['GET'])
def obtener_turnos_medicos_json(id_search):
    medico = obtener_medico_id(id_search)
    
    if medico:
        turnos_medicos = obtener_turnos_medicos(id_search)
        
        if turnos_medicos:
            # Convertir la lista de turnos a una lista de diccionarios
            turnos_dict = [turno.turno_dict() for turno in turnos_medicos]

            # Convertir las timedelta a cadenas en cada diccionario
            for turno_dict in turnos_dict:
                turno_dict['hora'] = str(turno_dict['hora'])

            return jsonify(turnos_dict), 200
        else:
            return jsonify({'error': 'No hay turnos para este medico'}), 404
    else:
        return jsonify({'error': 'El medico buscado no existe'}), 404


    
@turnos_bp.route('/turnos/<int:id_turno>', methods=['DELETE']) 
def eliminar_turno(id_turno):
            turno = turno_eliminado(id_turno)
            if turno:
                return jsonify({'exito':'Turno eliminado exitosamente'}),200
            else:
                return jsonify({'error': 'El turno buscando no existe'}),404
     

@turnos_bp.route('/turnos', methods=['POST'])
def crear_turno():
    if request.is_json:
        data = request.get_json()
        if 'id_medico' and 'id_paciente' and 'hora' and 'fecha' in data:
            if obtener_medico_id(data['id_medico']):
                if obtener_paciente_id(data['id_paciente']):
                    if formato_hora(data['hora']):
                        if validar_fecha(data['fecha']):
                            if verificar_turno_creado(data['id_medico'], data['hora'], data['fecha']):
                                if data['hora'][-2:] in ['00', '15', '30', '45']:
                                    if verificar_habilitacion_medico(data['id_medico']):
                                        turn= agregar_turno(data)
                                        if turn:
                                            turn_dict = turn.turno_dict()
                                            turn_dict['hora'] = str(turn_dict['hora'])
                                            return jsonify(turn_dict),201
                                        else:
                                            return jsonify({'error': 'No se pudo crear el turno'}),400
                                    else:
                                        return jsonify({'error':'El medico no se encuentro habilitado para atender'})
                                else:
                                    return jsonify({'error': 'Los turnos se dan cada 15 minutos, ej: HH:00, HH:15, HH:30, HH:45'})
                            else:
                                return jsonify({'error':'El doctor posee ya posee un turno para este horario y dia'}),400
                        else:
                            return jsonify({'error':'La fecha solicitada es menor o se pasa del plazo de 30 dias, porfavor utilizar el formato Y-M-D'}),404
                    else: 
                        return jsonify({'error': 'La hora no tiene el formato correcto de tipo HH:MM'}),400
                else:
                    return jsonify({'error': 'El paciente buscando no existe'}),404
            else:
                return jsonify({'error': 'El medico buscando no existe'}),404
        else:
            return jsonify({'error': 'No se completaron los campos debidamente'}),400
    else:
        return jsonify({'error': 'No se enviaron los datos correctamente'}),400



@turnos_bp.route('/turnos/pendiente/<int:id_turno>', methods=['GET'])  # Ruta para mostrar los turnos pendientes
def obtener_turnos_pendientes(id_turno):
    turnos = turnos_pendientes(id_turno)

    if len(turnos) > 0:
        # Crear una lista de diccionarios para representar cada turno
        turnos_dicts = [turno.turno_dict() for turno in turnos]

        # Convertir las horas a cadenas para asegurar la serialización JSON
        for turno_dict in turnos_dicts:
            turno_dict['hora'] = str(turno_dict['hora'])

        return jsonify(turnos_dicts), 200
    else:
        return jsonify({'error': 'No hay más turnos pendientes por hoy'}), 400
