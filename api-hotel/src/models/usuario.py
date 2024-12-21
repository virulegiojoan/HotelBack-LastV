from models import db
from sqlalchemy import Enum
import enum


class TipoUsuarioEnum(str, enum.Enum):
    CLIENTE = "CLIENTE"
    EMPLEADO = "EMPLEADO"


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(25), nullable=False, unique=True)
    categoria = db.Column(Enum(TipoUsuarioEnum), nullable=False)
    clave = db.Column(db.String(255), nullable=False)
    email=db.Column(db.String(255), nullable=False)

    reservas = db.relationship('Reserva', backref='usuario', lazy=True)

    def __init__(self, usuario=None, categoria=None, clave=None):
        self.usuario = usuario
        self.categoria = categoria
        self.clave = clave
    
   
        