from models import db

class Habitacion(db.Model):
    __tablename__ = 'habitaciones'

    id = db.Column(db.Integer, primary_key=True)
    numeroHabitacion = db.Column(db.Integer, unique=True, nullable=False)
    precioPorDia = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True, nullable=False)

    reservas = db.relationship('Reserva', backref='habitacion', lazy=True)

    def __init__(self, numeroHabitacion=None, precioPorDia=None, disponible=None):
        self.numeroHabitacion = numeroHabitacion
        self.precioPorDia = precioPorDia
        self.disponible = disponible