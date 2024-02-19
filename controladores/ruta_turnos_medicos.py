from flask import Blueprint,request,jsonify
from modelos.turnos import obtener_turnos_medicos, turno_eliminado, turno_agregado, validar_fecha, verificar_turno_creado, turnos_pendientes
from modelos.medicos import obtener_medico_id, verificar_habilitacion_medico
from modelos.pacientes import obtener_paciente_id
from modelos.agenda_medicos import formato_hora

turnos_bp = Blueprint('turnos_bp', __name__)

@turnos_bp.route('/turnos/<int:search_id>', methods=['GET'])
def obtener_turnos_medicos_json(search_id):
    if obtener_medico_id(search_id):
        turno_medico = obtener_turnos_medicos(search_id)
        if turno_medico:
            return jsonify(turno_medico),200
        else:
            return jsonify({'error': 'No hay turnos para este medico'}),404
    else:
        return jsonify({'error': 'El medico buscando no existe'}),404
    
@turnos_bp.route('/turnos/<int:id_medico>/<int:id_paciente>', methods=['DELETE']) # Fue la unica manera en la que se me ocurrio para realizar la validacion con los dos id
def eliminar_turno(id_medico, id_paciente):
    if obtener_medico_id(id_medico):
        if obtener_paciente_id(id_paciente):
            turno = turno_eliminado(id_medico, id_paciente)
            if turno:
                return jsonify(turno),200
            else:
                return jsonify({'error': 'El turno buscando no existe'}),404
        else:
            return jsonify({'error': 'El paciente buscando no existe'}),404
    else:
        return jsonify({'error': 'El medico buscando no existe'}),404

@turnos_bp.route('/turnos', methods=['POST'])
def crear_turno():
    if request.is_json:
        data = request.get_json()
        if 'id_medico' and 'id_paciente' and 'hora_turno' and 'fecha_solicitud' in data:
            if obtener_medico_id(data['id_medico']):
                if obtener_paciente_id(data['id_paciente']):
                    if formato_hora(data['hora_turno']):
                        if validar_fecha(data['fecha_solicitud']):
                            if verificar_turno_creado(data['id_medico'], data['hora_turno'], data['fecha_solicitud']):
                                if data['hora_turno'][-2:] in ['00', '15', '30', '45']:
                                    if verificar_habilitacion_medico(data['id_medico']):
                                        turno = turno_agregado(data)
                                        if turno:
                                            return jsonify(turno),201
                                        else:
                                            return jsonify({'error': 'No se pudo crear el turno'}),400
                                    else:
                                        return jsonify({'error':'El medico no se encuentro habilitado para atender'})
                                else:
                                    return jsonify({'error': 'Los turnos se dan cada 15 minutos, ej: HH:00, HH:15, HH:30, HH:45'})
                            else:
                                return jsonify({'error':'El doctor posee ya posee un turno para este horario y dia'}),400
                        else:
                            return jsonify({'error':'La fecha solicitada es menor o se pasa del plazo de 30 dias, porfavor utilizar el formato Y/M/D'}),404
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


@turnos_bp.route('/turnos', methods=['GET'])  #Ruta para mostrar los turnos pendientes
def obtener_turnos_pendientes():
    turnos = turnos_pendientes()

    if len(turnos) > 0:
        return jsonify(turnos),200
    else:
        return jsonify({'error':'No hay mas turnos penidentes por hoy'}),400