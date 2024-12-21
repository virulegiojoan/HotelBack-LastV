from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from schemas import ma
from marshmallow import fields
from models import Habitacion
from models.reserva import Reserva 
from models.usuario import Usuario

class HabitacionSchema(ma.SQLAlchemySchema):

    id = fields.Integer(data_key="id")
    numeroHabitacion = fields.Integer(data_key="numero")
    precioPorDia = fields.Float(data_key="precio")
    disponible = fields.Boolean(data_key="activa")
    
    reservas = fields.Nested(lambda: ReservaSchema(many=True, exclude=["habitacion"] ), data_key="reservas")
    
    estado = fields.Method("get_estado", data_key="estado")

    def get_estado(self, habitacion):
        porFecha = self.context.get("porFecha")
        if porFecha:
            tiene_reserva = any(
                reserva.fechaInicioReserva <= porFecha <= reserva.fechaFinReserva
                for reserva in habitacion.reservas
            )
            return "ocupada" if tiene_reserva else "libre"
        return "desconocido"


class UsuarioSchema(ma.SQLAlchemySchema):
  
    id = fields.Integer(data_key="id")
    usuario = fields.String(data_key="user")
    categoria = fields.Float(data_key="tipo_usuario")
    disponible = fields.Boolean(data_key="disponibilidad")
    
    reserva = fields.Nested(lambda: ReservaSchema(many=True, exclude=["usuario"] ), data_key="usuario")


class ReservaSchema(ma.SQLAlchemyAutoSchema):
    
    id = fields.Integer(data_key="id")
    fechaInicioReserva = fields.Date(data_key="inicio")
    fechaFinReserva = fields.Date(data_key="fin")
    habitacion_num = fields.Function(lambda r: r.habitacion.numeroHabitacion, data_key="numero")
    precioPorDia = fields.Function(lambda r: r.habitacion.precioPorDia, data_key="precio")

    habitacion = fields.Nested(lambda: HabitacionSchema(many=False, exclude=["reserva"] ), data_key="habitaciones")
    usuario = fields.Function( lambda r: r.usuario.usuario, data_key="usuario")

class ReservaSchemaHab(ma.SQLAlchemyAutoSchema):
    
    id = fields.Integer(data_key="id")
    fechaInicioReserva = fields.Date(data_key="inicio")
    fechaFinReserva = fields.Date(data_key="fin")
    habitacion_num = fields.Function(lambda h: h.numeroHabitacion, data_key="numero")
    precioPorDia = fields.Function(lambda h: h.precioPorDia, data_key="precio")

    habitacion = fields.Nested(lambda: HabitacionSchema(many=False, exclude=["reserva"] ), data_key="habitaciones")
    usuario = fields.Function( lambda r: r.usuario.usuario, data_key="usuario")
