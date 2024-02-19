from flask import Blueprint, jsonify, request
from modelos.pacientes import obtener_lista_pacientes, obtener_paciente_id, agregar_paciente, modificar_paciente

pacientes_bp = Blueprint('pacientes', __name__) 

@pacientes_bp.route('/pacientes', methods=['GET'])
def obtener_lista_pacientes_json():
    pacientes = obtener_lista_pacientes()

    if len(pacientes) > 0:
        return jsonify(pacientes),200
    else:
        return jsonify({'error':'No hay ningun paciente registrado'}),404
    
@pacientes_bp.route('/pacientes/<int:id_search>', methods=['GET'])
def obtener_paciente_id_json(id_search):
    paciente = obtener_paciente_id(id_search)

    if paciente:
        return jsonify(paciente),200
    else:
        return jsonify({'error':'paciente no encontrado'}),404
    
@pacientes_bp.route('/pacientes', methods=['POST'])
def agregar_paciente_json():
    if request.is_json:
        data = request.get_json()
        if 'dni' and 'nombre' and 'apellido' and 'telefono' and 'email' and 'direccion_calle' and 'direccion_numero' in data:
            paciente = agregar_paciente(data)
            return jsonify(paciente),200
        else: 
            return jsonify({'error':'faltan campos por completar'}),404
    else:
        return jsonify({'error':'no se recibieron los datos en formato json'}),404


@pacientes_bp.route('/pacientes/<int:id_search>', methods=['PUT'])
def modificar_paciente_json(id_search):
    

    if request.is_json:
        data = request.get_json()
        if 'dni' and 'nombre' and 'apellido' and 'telefono' and 'email' and 'direccion_calle' and 'direccion_numero' in data:
            paciente = modificar_paciente(id_search,data)
            if paciente:
                return jsonify(paciente),200
            else:
                return jsonify({'error':'paciente no encontrado'}),404
        else:
            return jsonify({'error':'faltan campos por completar'}),404
    else:
        return jsonify({'error':'no se recibieron los datos en formato json'}),404