from flask import Blueprint, jsonify, request
from modelos.medicos import obtener_lista_medicos, obtener_medico_id, agregar_medico,modificar_medico, desabilitar_medico, medico_existe

medicos_bp = Blueprint('medicos',__name__)

@medicos_bp.route('/medicos', methods=['GET'])
def obtener_lista_medicos_json():
    medicos = obtener_lista_medicos()

    if len(medicos) > 0:
        return jsonify(medicos),200
    else:
        return jsonify({'error':'No hay ningun medico registrado'}),404
    
@medicos_bp.route('/medicos/<int:id_search>', methods=['GET'])
def obtener_medico_id_json(id_search):
    medico = obtener_medico_id(id_search)

    if medico:
        return jsonify(medico),200
    else:
        return jsonify({'error':'medico no encontrado'}),404
    
@medicos_bp.route('/medicos', methods=['POST'])
def agregar_medico_json():
    if request.is_json:
        data = request.get_json()
        if 'dni' and 'nombre' and 'apellido' and 'matricula' and 'telefono' and 'email' in data:
                medico = agregar_medico(data)
                return jsonify(medico),200
        else: 
            return jsonify({'error':'faltan campos por completar'}),404
    else:
        return jsonify({'error':'no se recibieron los datos en formato json'}),404


@medicos_bp.route('/medicos/<int:id_search>', methods=['PUT'])
def modificar_medico_json(id_search):
    

    if request.is_json:
        data = request.get_json()
        if 'dni' and 'nombre' and 'apellido' and 'matricula' and 'telefono' and 'email' in data:
            medico = modificar_medico(id_search,data)
            if medico:
                return jsonify(medico),200
            else:
                return jsonify({'error':'medico no encontrado'}),404
        else:
            return jsonify({'error':'faltan campos por completar'}),404
    else:
        return jsonify({'error':'no se recibieron los datos en formato json'}),404
    
@medicos_bp.route('/medicos/desabilitar/<int:id_search>', methods=['PUT'])
def desabilitar_medico_json(id_search):

    medico = desabilitar_medico(id_search)

    if medico:
        return jsonify(medico),200
    else:
        return jsonify({'error':'medico no encontrado'}),404