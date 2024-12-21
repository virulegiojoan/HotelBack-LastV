from models import db
from schemas import ma
from marshmallow import fields, validate

ValidarLongitud= validate.Length(min=6, max=10)


class AltaUser(ma.Schema):
    email = fields.Str(required=True)
    categoria= fields.Str(required=True)
    clave1= fields.Str(required=True)
    clave2= fields.Str(required=True)

class LoginUser(ma.Schema):
    usuario = fields.Str(required=True)
    clave= fields.Str(required=True, validate=ValidarLongitud)



class AltaHabitacion(ma.Schema):
    numero= fields.Int(required=True)
    precio= fields.Float(required=True)


class AltaReserva(ma.Schema):
    inicio= fields.Date(required=True, format='%d/%m/%Y')
    fin= fields.Date(required=True, format='%d/%m/%Y')
    habitacion= fields.Int(required=True)
    
class EditarPrecio(ma.Schema):
    precio= fields.Float(required=True)

class EditarHabitacion(ma.Schema):
    disponible= fields.Str(required=True)







