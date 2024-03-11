from flask import Blueprint, jsonify, request
from modelos.pacientes import obtener_lista_pacientes, obtener_paciente_dni, agregar_paciente, modificar_paciente,deshabilitar_paciente, habilitar_paciente, eliminar_paciente

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/pacientes', methods=['GET'])
def obtener_lista_pacientes_json():
    pacientes = obtener_lista_pacientes()

    if len(pacientes) > 0:
        return jsonify([paciente.as_dict() for paciente in pacientes]), 200
    else:
        return jsonify({'error': 'No hay ningún paciente registrado'}), 404

@pacientes_bp.route('/pacientes/<string:dni_search>', methods=['GET'])
def obtener_paciente_id_json(dni_search):
    paciente = obtener_paciente_dni(dni_search)

    if paciente:
        return jsonify(paciente.paciente_dict()), 200
    else:
        return jsonify({'error': f'Paciente con DNI {dni_search} no encontrado'}), 404

@pacientes_bp.route('/pacientes', methods=['POST'])
def agregar_paciente_json():
    if request.is_json:
        data = request.get_json()
        if 'dni_paciente' in data and 'nombre_paciente' in data and 'apellido_paciente' in data and 'telefono_paciente' in data and 'email_paciente' in data and 'direccion_calle' in data and 'direccion_numero' in data:
            paciente = agregar_paciente(data)
            if paciente:
                return jsonify(paciente.paciente_dict()), 200
            else:
                return jsonify({'error': 'Ya existe el paciente'}), 400
        else:
            return jsonify({'error': 'Faltan campos por completar'}), 404
    else:
        return jsonify({'error': 'No se recibieron los datos en formato json'}), 404

@pacientes_bp.route('/pacientes/<string:dni_search>', methods=['PUT'])
def modificar_paciente_json(dni_search):
    paciente = obtener_paciente_dni(dni_search)

    if paciente:
        if request.is_json:
            data = request.get_json()
            if 'dni_paciente' in data or 'nombre_paciente' in data or 'apellido_paciente' in data or 'telefono_paciente' in data or 'email_paciente' in data or 'direccion_calle' in data or 'direccion_numero' in data:
                paciente_modificado, error = modificar_paciente(dni_search, data)
                if paciente_modificado:
                    return jsonify(paciente_modificado.paciente_dict()), 200
                elif error and ('El' in error['error'] or 'La' in error['error']) and 'ya está en uso por otro paciente' in error['error']:
                    return jsonify(error), 400
                else:
                    return jsonify({'error': 'Paciente no encontrado'}), 404
            else:
                return jsonify({'error': 'Faltan campos por completar'}), 404
        else:
            return jsonify({'error': 'No se recibieron los datos en formato json'}), 404
    else:
        return jsonify({'error': f'Paciente con DNI {dni_search} no encontrado'}), 404

# En 'rutas_pacientes.py'

@pacientes_bp.route('/pacientes/deshabilitar/<string:dni_search>', methods=['PUT'])
def deshabilitar_paciente_json(dni_search):
    paciente = deshabilitar_paciente(dni_search)

    if paciente:
        return jsonify(paciente.paciente_dict()), 200
    else:
        return jsonify({'error': 'Paciente no encontrado'}), 404

@pacientes_bp.route('/pacientes/habilitar/<string:dni_search>', methods=['PUT'])
def habilitar_paciente_json(dni_search):
    paciente = habilitar_paciente(dni_search)

    if paciente:
        return jsonify(paciente.paciente_dict()), 200
    else:
        return jsonify({'error': 'Paciente no encontrado'}), 404


@pacientes_bp.route('/pacientes/<string:dni_search>', methods=['DELETE'])
def eliminar_paciente_json(dni_search):
    paciente = eliminar_paciente(dni_search)

    if paciente:
        return jsonify(paciente.paciente_dict()), 200
    else:
        return jsonify({'error': 'Paciente no encontrado'}), 404
    
