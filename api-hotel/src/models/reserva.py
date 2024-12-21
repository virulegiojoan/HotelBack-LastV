from models import db

class Reserva(db.Model):
    __tablename__ ='reservas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    habitacion_num = db.Column(db.Integer, db.ForeignKey('habitaciones.numeroHabitacion'), nullable=False)
    fechaInicioReserva = db.Column(db.Date, nullable=False) 
    fechaFinReserva = db.Column(db.Date, nullable=False)  
    

    def __init__(self, usuario_id=None, habitacion_num=None , fechaInicioReserva=None, fechaFinReserva=None):
        self.usuario_id = usuario_id
        self.habitacion_num  = habitacion_num 
        self.fechaInicioReserva = fechaInicioReserva
        self.fechaFinReserva = fechaFinReserva
