from app import db
from sqlalchemy import and_
from sqlalchemy.orm import relationship

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id_paciente = db.Column(db.Integer, unique=True, primary_key=True)
    dni_paciente = db.Column(db.String(10), unique=True, nullable=False)
    nombre_paciente = db.Column(db.String(100), nullable=False)
    apellido_paciente = db.Column(db.String(100), nullable=False)
    telefono_paciente = db.Column(db.String(100), unique=True, nullable=False)
    email_paciente = db.Column(db.String(100), unique=True, nullable=False)
    direccion_calle = db.Column(db.String(100), nullable=False)
    direccion_numero = db.Column(db.String(100), nullable=False)
    habilitado = db.Column(db.Integer, nullable=False)

    turnos = relationship('Turno', back_populates='paciente')  #Relacion bidireccional con la tabla 'turnos'

    def paciente_dict(self):
        return {
            'id_paciente': self.id_paciente,
            'dni_paciente': self.dni_paciente,
            'nombre_paciente': self.nombre_paciente,
            'apellido_paciente': self.apellido_paciente,
            'telefono_paciente': self.telefono_paciente,
            'email_paciente': self.email_paciente,
            'direccion_calle': self.direccion_calle,
            'direccion_numero': self.direccion_numero,
            'habilitado': self.habilitado
        }

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

def obtener_lista_pacientes():
    return Paciente.query.all()

def obtener_paciente_dni(dni_search):
    return Paciente.query.filter_by(dni_paciente=dni_search).first()

def obtener_paciente_id(id_search):
    return Paciente.query.get(id_search)

def agregar_paciente(data):
    existe_dni = Paciente.query.filter_by(dni_paciente=data['dni_paciente']).first()
    existe_email = Paciente.query.filter_by(email_paciente=data['email_paciente']).first()

    if existe_dni or existe_email:
        return None
    
    paciente = Paciente(
        dni_paciente=data['dni_paciente'],
        nombre_paciente=data['nombre_paciente'],
        apellido_paciente=data['apellido_paciente'],
        telefono_paciente=data['telefono_paciente'],
        email_paciente=data['email_paciente'],
        direccion_calle=data['direccion_calle'],
        direccion_numero=data['direccion_numero'],
        habilitado=1
    )

    db.session.add(paciente)
    db.session.commit()

    return paciente

def modificar_paciente(dni_search, data):
    existe = obtener_paciente_dni(dni_search)

    if existe:
        query_filters = []

        if 'dni_paciente' in data:
            query_filters.append(and_(Paciente.id_paciente != existe.id_paciente, Paciente.dni_paciente == data['dni_paciente']))
        if 'email_paciente' in data:
            query_filters.append(and_(Paciente.id_paciente != existe.id_paciente, Paciente.email_paciente == data['email_paciente']))
        if 'telefono_paciente' in data:
            query_filters.append(and_(Paciente.id_paciente != existe.id_paciente, Paciente.telefono_paciente == data['telefono_paciente']))

        existing_patient = Paciente.query.filter(*query_filters).first()

        if existing_patient:
            campo_en_uso = next((campo for campo in ['dni_paciente', 'email_paciente', 'telefono_paciente'] if campo in data), None)
            return None, {'error': f'El {campo_en_uso} ya está en uso por otro paciente'}
        
        for key, value in data.items():
            setattr(existe, key, value)

        db.session.commit()

        return existe, None

    return None, {'error': f'Paciente con DNI {dni_search} no encontrado'}

def deshabilitar_paciente(dni_search):
    existe = obtener_paciente_dni(dni_search)

    if existe:
        existe.habilitado = 0
        db.session.commit()
        return existe

    return None

def habilitar_paciente(dni_search):
    existe = obtener_paciente_dni(dni_search)

    if existe:
        existe.habilitado = 1
        db.session.commit()
        return existe

    return None

def eliminar_paciente(dni_search):
    try:
        existe = obtener_paciente_dni(dni_search)

        if existe:

            db.session.delete(existe)
            db.session.commit()

            return existe

    except Exception as e:
        print(f"Error durante la eliminación: {e}")

    return None

