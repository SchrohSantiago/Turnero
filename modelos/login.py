from modelos.pacientes import Paciente
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from modelos.jwt_utils import generar_token, validar_token


def agregar_register(data):
    existe_dni = Paciente.query.filter_by(dni_paciente=data['dni_paciente']).first()
    existe_email = Paciente.query.filter_by(email_paciente=data['email_paciente']).first()

    if existe_dni or existe_email:
        return None
    
    hashed_password = generate_password_hash(data['password_paciente'])  # Utilizamos BCRYPT para encriptar el password
    paciente = Paciente(
        dni_paciente=data['dni_paciente'],
        nombre_paciente=data['nombre_paciente'],
        apellido_paciente=data['apellido_paciente'],
        telefono_paciente=data['telefono_paciente'],
        email_paciente=data['email_paciente'],
        password_paciente=hashed_password,   
        direccion_calle=data['direccion_calle'],
        direccion_numero=data['direccion_numero'],
        habilitado=1
    )

    db.session.add(paciente)
    db.session.commit()

    return paciente

def verificar_email(email):
    return Paciente.query.filter_by(email_paciente=email).first()


def verificar_password(email, password):
    paciente = verificar_email(email)
    if paciente:
        return check_password_hash(paciente.password_paciente, password)
    else:
        return False

def cambiar_password(email, nueva_password):
    paciente = verificar_email(email)
    if paciente:
        hashed_password = generate_password_hash(nueva_password)
        paciente.password_paciente = hashed_password
        db.session.commit()
        return True
    else:
        return False
    
