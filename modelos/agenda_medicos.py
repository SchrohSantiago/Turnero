from datetime import datetime
from app import db
from sqlalchemy.orm import relationship

class Agenda_Medico(db.Model):
    __tablename__ = 'agenda_medicos'

    id_agenda = db.Column(db.Integer, unique=True, primary_key=True)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id_medico'), nullable=False)
    dia_numero = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.String(20), nullable=False)
    hora_fin = db.Column(db.String(20), nullable=False)
    fecha_actualizacion = db.Column(db.String(20), nullable=False, default=str(datetime.now()))

    medico = relationship('Medico', back_populates='agenda_medico')
   
    def agenda_dict(self):
        return {
            'id_agenda': self.id_agenda,
            'medico': self.medico.medic_dict(),
            'dia_numero': self.dia_numero,
            'hora_inicio': self.hora_inicio,
            'hora_fin': self.hora_fin,
            'fecha_actualizacion': self.fecha_actualizacion,  # Convertir a cadena de texto
        }


def obtener_agenda_medicos():
    # Imprimir instancias de objetos, no la clase
    agenda_medico_instances = Agenda_Medico.query.order_by(Agenda_Medico.dia_numero, Agenda_Medico.hora_inicio).all()

    return agenda_medico_instances
    

def agregar_agenda_medico(data):
    # Agregar un nuevo agenda
    agenda_nuevo = Agenda_Medico(
        id_medico=data['id_medico'],
        dia_numero=data['dia_numero'],
        hora_inicio=data['hora_inicio'],
        hora_fin=data['hora_fin'],
        fecha_actualizacion=str(datetime.now())
    )

    db.session.add(agenda_nuevo)
    db.session.commit()

    return agenda_nuevo

   

def formato_hora(hora): 
    try:
        datetime.strptime(hora, '%H:%M')
        return True
    except ValueError:
        return False
    
def validar_turno_existente(id_medico, dia_numero):

    if Agenda_Medico.query.filter_by(id_medico=id_medico, dia_numero=dia_numero).first():
        return False
    else:
        return True


def modificar_horarios_agenda(id, data):
    agenda = Agenda_Medico.query.filter_by(id_agenda=id).first()

    if agenda:
        # Actualizar los campos de la agenda con los nuevos valores
        agenda.hora_inicio = data['hora_inicio']
        agenda.hora_fin = data['hora_fin']

        # Confirmar los cambios en la base de datos
        db.session.commit()

        return agenda
    else:
        # Manejar el caso donde no se encuentra la agenda con el ID dado
        return None


def desabilitar_agenda_medico(id_medico):
    agendas = Agenda_Medico.query.filter_by(id_medico=id_medico).all()

    for agenda in agendas:
        db.session.delete(agenda)

    db.session.commit()

    return agendas

        # Manejar el caso donde no se encuentra la agenda


# def validar_horario_turno(id_medico, dia_numero, hora_inicio):
#     import_csv()
#     global agenda_medicos

#     # Buscar la agenda del médico y día específico
#     for agenda in agenda_medicos:
#         if agenda['id_medico'] == id_medico and agenda['dia_numero'] == dia_numero:
    
#             hora_inicio_turno = datetime.strptime(hora_inicio, '%H:%M').time()


#             # Verificar si las horas del turno están dentro del rango de horas laborales
          
#     return True


def validar_intervalo_15_minutos(hora_inicio, hora_fin):
    # Verificar si la diferencia entre la hora de inicio y la hora de fin es un múltiplo de 15 minutos
    diferencia = datetime.combine(datetime.today(), hora_fin) - datetime.combine(datetime.today(), hora_inicio)
    minutos = diferencia.total_seconds() / 60
    return minutos % 15 == 0