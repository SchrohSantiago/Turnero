from app import db
from sqlalchemy import and_
from sqlalchemy.orm import relationship



class Medico(db.Model):
    __tablename__ = 'medicos'

    id_medico = db.Column(db.Integer, unique=True, primary_key=True)
    dni = db.Column(db.String(10), unique=True, nullable=False)
    nombre_medico = db.Column(db.String(100), nullable=False)
    apellido_medico = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(100),unique=True, nullable=False)
    telefono = db.Column(db.String(100), unique=True,nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    habilitado = db.Column(db.Integer, nullable=False)

    turnos = relationship('Turno', back_populates='medico')
    agenda_medico = relationship('Agenda_Medico', back_populates='medico')

    def medic_dict(self):
        return {
            'id_medico': self.id_medico,
            'dni': self.dni,
            'nombre_medico': self.nombre_medico,
            'apellido_medico': self.apellido_medico,
            'matricula': self.matricula,
            'telefono': self.telefono,
            'email': self.email,
            'habilitado': self.habilitado
        }

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

def obtener_lista_medicos():
    return Medico.query.all()

def obtener_medico_dni(dni_search):
    return Medico.query.filter_by(dni=dni_search).first()

def obtener_medico_id(id_search):
    return Medico.query.get(id_search)


def agregar_medico(data):
    existe_dni = Medico.query.filter_by(dni=data['dni']).first()
    existe_email = Medico.query.filter_by(email=data['email']).first()

    if existe_dni or existe_email:
        return None
         
    
    medico = Medico(
        dni=data['dni'],
        nombre_medico=data['nombre_medico'],
        apellido_medico=data['apellido_medico'],
        matricula=data['matricula'],
        telefono=data['telefono'],
        email=data['email'],
        habilitado=1
    )

    db.session.add(medico)
    db.session.commit()  # Refrescamos los cambios en la base de datos 

    return medico


def modificar_medico(dni_search, data):
    # Obtener el médico existente
    existe = obtener_medico_dni(dni_search)

    if existe:
        # Verificar si se proporcionó dni, email, teléfono o matrícula en los datos
        
        # Construir filtros de consulta para cada campo
        query_filters = []

        if 'dni' in data:
            query_filters.append(and_(Medico.id_medico != existe.id_medico, Medico.dni == data['dni']))
        if 'email' in data:
            query_filters.append(and_(Medico.id_medico != existe.id_medico, Medico.email == data['email']))
        if 'telefono' in data:
            query_filters.append(and_(Medico.id_medico != existe.id_medico, Medico.telefono == data['telefono']))
        if 'matricula' in data:
            query_filters.append(and_(Medico.id_medico != existe.id_medico, Medico.matricula == data['matricula']))


        # Realizar la consulta para verificar si ya existe otro médico con los mismos datos
        existing_doctor = Medico.query.filter(*query_filters).first()

        if existing_doctor:
            campo_en_uso = next((campo for campo in ['dni', 'email', 'telefono','matricula'] if campo in data), None)
            if campo_en_uso == 'matricula':
                return None, {'error': f'La {campo_en_uso} ya está en uso por otro médico'}
            elif campo_en_uso == 'dni' or campo_en_uso == 'email' or campo_en_uso == 'telefono':
                return None, {'error': f'El {campo_en_uso} ya está en uso por otro médico'}
        
        
        # Actualizar solo los campos proporcionados
        for key, value in data.items():
            setattr(existe, key, value)

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return existe, None

    return None, {'error': f'Médico con DNI {dni_search} no encontrado'}


def deshabilitar_medico(dni_search):
    # Obtener el médico existente
    existe = obtener_medico_dni(dni_search)

    existe.habilitado = 0
    db.session.commit()

    return existe

def habilitar_medico(dni_search):

    existe = obtener_medico_dni(dni_search)

    existe.habilitado = 1
    db.session.commit()

    return existe

def eliminar_medico(dni_search):
    try:
        existe = obtener_medico_dni(dni_search)

        if existe:

            # Eliminar el médico de la sesión y confirmar los cambios en la base de datos
            db.session.delete(existe)
            db.session.commit()

            # Devolver el médico eliminado
            return existe

    except Exception as e:
        print(f"Error durante la eliminación: {e}")

    return None


def verificar_habilitacion_medico(id_search):
    existe = obtener_medico_id(id_search)

   
    if existe.habilitado == 1:
        return True
    else:
        return False
