from datetime import datetime
from app import db
from sqlalchemy.orm import relationship
from modelos.medicos import Medico


class Turno(db.Model):
    __tablename__ = 'turnos'

    id_turno = db.Column(db.Integer, unique=True, primary_key=True)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id_medico'), nullable=False)  #Debemos indicar de que tabla provienen estas ForeignKey
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    estado = db.Column(db.String, server_default='Pendiente')
    hora = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)


    medico = relationship('Medico', back_populates='turnos')
    paciente = relationship('Paciente', back_populates='turnos')
    

    def turno_dict(self):
        return {
            'id_turno': self.id_turno,
            'id_medico': self.id_medico,  
            'paciente': self.paciente.paciente_dict(),
            'estado': self.estado,
            'hora': self.hora,
            'fecha': self.fecha
        }

def obtener_turnos_medicos(id_search):
    return Turno.query.filter_by(id_medico=id_search).all()



def turno_eliminado(id_turno): 
    turno_eliminar = Turno.query.get(id_turno)

    if turno_eliminar:
       
        db.session.delete(turno_eliminar)
        db.session.commit()
        return turno_eliminar
   
    return None

    
def agregar_turno(data):
       
    nuevo_turno = Turno(
        id_medico=data['id_medico'],
        id_paciente=data['id_paciente'],
        hora=data['hora'],
        fecha=data['fecha']
    )

    
    db.session.add(nuevo_turno)
    db.session.commit()

    return nuevo_turno


def validar_fecha(fecha): 
    try:
        fecha_ingresada = datetime.strptime(fecha, '%Y-%m-%d').date()
        fecha_actual = datetime.now().date()
        
        # Verificar si la fecha es el día actual o posterior al día actual
        if fecha_ingresada >= fecha_actual:
            # Calcular la diferencia en días entre la fecha ingresada y la actual
            diferencia_dias = (fecha_ingresada - fecha_actual).days

            # Verificar si la diferencia es menor o igual a 30 días
            if 0 <= diferencia_dias <= 30:
                return True
            else:
                return False
        else:
            return False
    except ValueError:
        # Capturar errores si el formato de la fecha no es válido
        return False

def verificar_turno_creado(id_medico, hora_turno, fecha_solicitud):
   
    turno_existente = Turno.query.filter_by(
        id_medico=id_medico,
        hora=hora_turno,
        fecha=fecha_solicitud
    ).first()

    
    return turno_existente is None


def turnos_pendientes(id_medico):
    ahora = datetime.now()

    turnos_pendientes = (
    db.session.query(Turno)
        .join(Medico)
        .filter(Turno.id_medico == id_medico)
        .filter(db.func.concat(Turno.fecha, ' ', Turno.hora).cast(db.DateTime) > ahora)
        .all()
)


    return turnos_pendientes
