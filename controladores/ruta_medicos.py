from flask import Blueprint, jsonify, request
from modelos.medicos import obtener_lista_medicos, obtener_medico_id, agregar_medico, modificar_medico,deshabilitar_medico, habilitar_medico, eliminar_medico

medicos_bp = Blueprint('medicos',__name__)

@medicos_bp.route('/medicos', methods=['GET'])
def obtener_lista_medicos_json():
    medicos = obtener_lista_medicos()

    if len(medicos) > 0:
        return jsonify([medico.as_dict() for medico in medicos]),200
    else:
        return jsonify({'error':'No hay ningun medico registrado'}),404
    
@medicos_bp.route('/medicos/<string:dni_search>', methods=['GET'])
def obtener_medico_id_json(dni_search):
    medicos = obtener_medico_id(dni_search)

    if medicos:
        return jsonify(medicos.medic_dict()),200
    else:
        return jsonify({'error':f'Médico con DNI {dni_search} no encontrado'}),404
    
@medicos_bp.route('/medicos', methods=['POST'])
def agregar_medico_json():
    if request.is_json:
        data = request.get_json()
        if 'dni' in data and 'nombre_medico' in data and 'apellido_medico' in data and 'matricula' in data and 'telefono' in data and 'email' in data:
            medico = agregar_medico(data)
            if medico:
                return jsonify(medico.medic_dict()), 200
            else:
                return jsonify({'error':'Ya existe el medico'}), 400
        else:
            return jsonify({'error': 'faltan campos por completar'}), 404
    else:
        return jsonify({'error': 'no se recibieron los datos en formato json'}), 404


@medicos_bp.route('/medicos/<string:dni_search>', methods=['PUT'])
def modificar_medico_json(dni_search):
    

    if request.is_json:
        data = request.get_json()
        if 'dni' in data or 'nombre_medico' in data or 'apellido_medico' in data or 'matricula' in data or 'telefono' in data or 'email' in data:
            medico, error = modificar_medico(dni_search,data)
            if medico:  
                return jsonify(medico.medic_dict()),200
            elif error and ('El' in error['error'] or 'La' in error['error']) and 'ya está en uso por otro médico' in error['error']:
                return jsonify(error), 400
            else:
                return jsonify({'error':'medico no encontrado'}),404
        else:
            return jsonify({'error':'faltan campos por completar'}),404
    else:
        return jsonify({'error':'no se recibieron los datos en formato json'}),404
    
@medicos_bp.route('/medicos/deshabilitar/<string:dni_search>', methods=['PUT'])
def deshabilitar_medico_json(dni_search):

    medico = deshabilitar_medico(dni_search)

    if medico:
        return jsonify(medico.medic_dict()),200
    else:
        return jsonify({'error':'medico no encontrado'}),404

@medicos_bp.route('/medicos/habilitar/<string:dni_search>', methods=['PUT'])
def habilitar_medico_json(dni_search):

    medico = habilitar_medico(dni_search)

    if medico:
        return jsonify(medico.medic_dict()),200
    else:
        return jsonify({'error':'medico no encontrado'}),404
    
@medicos_bp.route('/medicos/<string:dni_search>', methods=['DELETE'])
def eliminar_medico_json(dni_search):
    medico = obtener_medico_id(dni_search)

    if medico:
        return jsonify(medico.medic_dict()),200
    else:
        return jsonify({'error':'medico no encontrado'}),404
