from flask import Blueprint, jsonify, request
from modelos.agenda_medicos import obtener_agenda_medicos, agregar_agenda_medico, formato_hora, validar_turno_existente, modificar_horarios_agenda, desabilitar_agenda_medico
from modelos.medicos import obtener_medico_id

agenda_medicos_bp = Blueprint('agenda_medicos_bp', __name__)

@agenda_medicos_bp.route('/agenda_medicos', methods=['GET'])   # Filtra unicamente los horarios de agenda habiles, es decir si hay turnos de ayer no los muestra
def obtener_agenda_medicos_json():
    agenda_medicos = obtener_agenda_medicos()

    if len(agenda_medicos) > 0:
        return jsonify(agenda_medicos),200
    else:
        return jsonify({'error':'No hay agendas para ningun medico'}),404
    
@agenda_medicos_bp.route('/agenda_medicos', methods=['POST'])
def agregar_agenda_medico_json():

    if request.is_json:
        data = request.get_json()
        if 'id_medico' and 'dia_numero' and 'hora_inicio' and 'hora_fin' in data:
            if obtener_medico_id(int(data['id_medico'])):
                if int(data['dia_numero']) > -1 and int(data['dia_numero']) < 7:
                    if formato_hora(data['hora_inicio']) and formato_hora(data['hora_fin']):
                        if data['hora_inicio'] < data['hora_fin']:
                          if validar_turno_existente(data['id_medico'],data['dia_numero']):
                                agenda_medico = agregar_agenda_medico(data)
                                return jsonify(agenda_medico),200
                          else:
                              return jsonify({'error':'el horario de la agenda no esta disponible'}),404
                        else:
                            return jsonify({'error':'la hora de inicio del turno debe ser menor a la hora de finalizacion del turno'}),404
                    else:   
                        return jsonify({'error':'las horas deben estar en formato HH:MM'}),404
                else:
                    return jsonify({'error':'el dia_numero debe estar entre 0 y 6'}),404
            else:
                return jsonify({'error':'medico no encontrado'}),404
        else:
            return jsonify({'error':'faltan campos por completar'}),404
    else:
        return jsonify({'error':'no se recibieron los datos en formato json'}),404

@agenda_medicos_bp.route('/agenda_medicos/<int:id_search>', methods=['PUT'])
def modificar_agenda_medico_json(id_search):

    if request.is_json:
        data = request.get_json()
        if 'dia_numero' and 'hora_inicio' and 'hora_fin' in data:
            if obtener_medico_id(id_search):
                if int(data['dia_numero']) > -1 and int(data['dia_numero']) < 7:
                    if formato_hora(data['hora_inicio']) and formato_hora(data['hora_fin']):
                        if data['hora_inicio'] < data['hora_fin']:
                            if not validar_turno_existente(id_search,data['dia_numero']):
                                agenda_medico = modificar_horarios_agenda(id_search,data)
                                return jsonify(agenda_medico),200
                            else:
                                 return jsonify({'error':'en el dia introducido, el medico no trabaja'}),404
                        else:
                            return jsonify({'error':'la hora de inicio del turno debe ser menor a la hora de finalizacion del turno'}),404
                    else:
                        return jsonify({'error':'las horas deben estar en formato HH:MM'}),404
                else:
                    return jsonify({'error':'el dia_numero debe estar entre 0 y 6'}),404
            else:
                return jsonify({'error':'medico no encontrado'}),404
        else:
            return jsonify({'error':'faltan campos por completar'}),404
    else: 
        return jsonify({'error':'no se recibieron los datos en formato json'}),404
    
@agenda_medicos_bp.route('/agenda_medicos/<int:id_search>', methods=['DELETE'])
def desabilitar_agenda_medico_json(id_search):

    if obtener_medico_id(id_search):
        agenda_medico = desabilitar_agenda_medico(id_search)
        return jsonify(agenda_medico),200
    else:
        return jsonify({'error':'medico no encontrado'}),404