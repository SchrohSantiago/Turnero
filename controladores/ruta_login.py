from flask import Blueprint, jsonify, request
from modelos.login import agregar_register, verificar_email, verificar_password, cambiar_password
from modelos.jwt_utils import generar_token, validar_token
import secrets

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/register', methods=['POST'])
def register_json():
    if request.is_json:
        data = request.get_json()
        if 'dni_paciente' in data and 'nombre_paciente' in data and 'apellido_paciente' in data and 'telefono_paciente' in data and 'email_paciente' in data and 'direccion_calle' in data and 'direccion_numero' in data and 'password_paciente':
            paciente = agregar_register(data)
            if paciente: 
                clave_secreta = secrets.token_urlsafe(32)
                token = generar_token({'usuario_id': paciente.email_paciente}, clave_secreta, tiempo_expiracion_minutos=40)
                return jsonify(paciente.paciente_dict(), {'token':token}), 200
            else:
                return jsonify({'error': 'Ya existe el paciente'}), 400
        else:
            return jsonify({'error': 'Faltan campos por completar'}), 404
    else:
        return jsonify({'error': 'No se recibieron los datos en formato json'}), 404
    
@login_bp.route('/login', methods=['POST'])
def login_json():
    if request.is_json:
        data = request.get_json()
        if 'email_paciente' in data and 'password_paciente' in data:
            if verificar_email(data['email_paciente']):
                if verificar_password(data['email_paciente'],data['password_paciente']):
                    clave_secreta = secrets.token_urlsafe(32)
                    token = generar_token({'usuario_id': data['email_paciente']}, clave_secreta, tiempo_expiracion_minutos=40)
                    return jsonify({'exito' :'Datos correctos'}, {'token':token}), 200
                else:
                    return jsonify({'error': 'Contrasenia incorrecta'}), 404
            else:
               return jsonify({'error': 'Email no registrado'}), 404
        else:
            return jsonify({'error': 'Faltan campos por completar'}), 404
    else:
        return jsonify({'error': 'No se recibieron los datos en formato json'}), 404
    
@login_bp.route('/changepassword', methods=['PUT'])
def changepassword_json():
    if request.is_json:
        data = request.get_json()
        if 'email_paciente' in data and 'password_paciente' in data and 'nueva_password' in data:
            if verificar_email(data['email_paciente']):
                if verificar_password(data['email_paciente'],data['password_paciente']):
                    if cambiar_password(data['email_paciente'],data['nueva_password']):
                        return jsonify({'exito' :'Contraseña cambiada correctamente'}), 200
                    else:
                        return jsonify({'error': 'Error al cambiar la contraseña'}), 404
                else:
                    return jsonify({'error': 'Contrasenia incorrecta'}), 404
            else:
               return jsonify({'error': 'Email no registrado'}), 404
        else:
            return jsonify({'error': 'Faltan campos por completar'}), 404
    else:
        return jsonify({'error': 'No se recibieron los datos en formato json'}), 404


@login_bp.route('/recurso-protegido', methods=['GET'])  # Actualmente no tenemos creados endpoints para los recursos protegidos, dejamos este ejemplo para cuando por ejemplo el paciente desee modificar su perfil 
def recurso_protegido():  # Enrealidad si. si el paciente quiere obtener un turno debera tener un token de authenticacion
    token = request.headers.get('Authorization')
    if token:
        resultado_validacion = validar_token(token)
        if resultado_validacion:
            return jsonify({'mensaje': 'Acceso al recurso protegido permitido'}), 200
        else:
            return jsonify({'error': 'Token inválido o expirado'}), 401
    else:
        return jsonify({'error': 'Token no proporcionado'}), 401
