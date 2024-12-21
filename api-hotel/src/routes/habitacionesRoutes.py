from flask import Blueprint
from flask import request
from sqlalchemy import Date
from schemas import HabitacionSchema
from app import db
from models.habitacion import Habitacion
from datetime import datetime
from schemas import AltaHabitacion, EditarPrecio
from decorators.route_decorators import autenticadoCli, autenticadoEmple, json_mapped


habitaciones =Blueprint('habitaciones', __name__)

@habitaciones.route("/habitaciones", methods=['POST'])
@json_mapped(AltaHabitacion())
@autenticadoEmple()
def crearHabitacion(data=None, auth=None):
    habitacion= Habitacion()
    habitacion.numeroHabitacion=data['numero']
    habitacion.precioPorDia=data['precio']
    
    if Habitacion.query.filter(Habitacion.numeroHabitacion == habitacion.numeroHabitacion).first():
        return {"mensaje": "Ya existe una habitación con este numero"}

    db.session.add(habitacion)
    db.session.commit()
    return {
        "mensaje": "habitacion creada correctamente"
    }

@habitaciones.route("/habitaciones", methods=['GET'])
@autenticadoEmple()
def obtenerHabitaciones(auth):

    habitaciones= Habitacion.query.all()
    
    habitacion_disponible = Habitacion.query.filter_by(disponible=True).count()
    
    hSchema = HabitacionSchema(exclude = ['reservas', 'estado'], many=True)
    return {"habitaciones": hSchema.dump(habitaciones),
            "cantidad": habitacion_disponible
            }

@habitaciones.route("/habitaciones/<int:id>", methods=['GET'])
@autenticadoEmple()
def obtenerHabitacionPorId(id, auth):
    habitacion = Habitacion.query.filter( Habitacion.id == id).first()
    
    hSchema = HabitacionSchema( exclude = ['disponible','estado','reservas.precioPorDia','reservas.habitacion_num'] )
    return hSchema.dump(habitacion)


@habitaciones.route("/habitaciones/<int:id>/precio", methods=['PUT'])
@json_mapped(EditarPrecio())
@autenticadoEmple()
def actualizarPrecioHabitacion(id, data, auth=None):
    data = request.json

    habitacion = Habitacion.query.filter( Habitacion.id == id).first()

    
    habitacion.precioPorDia= data['precio']

    
    db.session.commit()

    return {"mensaje": "precio actualizado correctamente" }

@habitaciones.route("/habitaciones/<int:id>", methods=['DELETE'])
@autenticadoEmple()
def eliminarHabitacion(id, auth=None):
    
    habitacion = Habitacion.query.filter(Habitacion.id == id).first()
    if not habitacion:
        return {"mensaje": "Habitación no encontrada"}, 404
    
    if not habitacion.disponible:
        return {"mensaje": "La habitación ya está marcada como no disponible"}
    
    habitacion.disponible = False
    
    db.session.commit()
    
    return {"mensaje": "Habitación eliminada correctamente"}


@habitaciones.route("/habitaciones/<int:id>", methods=['POST'])
@autenticadoEmple()
def levantarHabitacion(id, auth=None):
    habitacion = Habitacion.query.filter(Habitacion.id == id).first()
    if not habitacion:
        return {"mensaje": "Habitación no encontrada"}, 404
    
    if habitacion.disponible:
        return {"mensaje": "La habitación ya está marcada como disponible"}
    
    habitacion.disponible = True
    
    db.session.commit()
    
    return {"mensaje": "Habitación levantada correctamente"}


@habitaciones.route("/habitaciones/filtrar", methods=['GET'])
@autenticadoCli()
def obtenerHabitacionesPorPrecio(auth):
    precioTope = request.args.get('precio', type=float)
    
    if precioTope is None:
        return {"error": "Debe proporcionar un valor para el parámetro 'precio'"}, 400

    
    habitaciones = Habitacion.query.filter(Habitacion.precioPorDia <= precioTope).all()

    hSchema = HabitacionSchema( exclude = ['disponible','reservas','estado'], many=True )
    return hSchema.dump(habitaciones)
  
  

@habitaciones.route("/habitaciones/diario", methods=['GET'])
@autenticadoEmple()
def obtenerHabitacionesPorFecha(auth):
    porFecha = request.args.get('fecha')
    
    try:
        porFecha = datetime.strptime(porFecha, '%d/%m/%Y').date()
    except ValueError:
        return {"error": "Formato de fecha inválido. Usa DD/MM/YYYY."}, 400

    habitaciones= Habitacion.query.all()
    
    habitacion_cant = len(habitaciones)
    
    hSchema = HabitacionSchema(exclude = ['reservas','id','precioPorDia','disponible'], many=True, context={"porFecha": porFecha})
    return {"habitaciones": hSchema.dump(habitaciones),
            "cantidad": habitacion_cant
            }

