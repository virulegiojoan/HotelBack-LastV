from flask import Blueprint
from flask import request
from schemas import ReservaSchema, HabitacionSchema
from models import Habitacion, habitacion
from app import db
from models.reserva import Reserva
from datetime import datetime
from schemas import AltaReserva
from decorators.route_decorators import autenticadoCli, autenticadoEmple, json_mapped
from schemas.schemas import ReservaSchemaHab


reservas = Blueprint('reservas', __name__)

#estamos traba2 y usuarios?
@reservas.route("/reservas", methods=['POST'])
@json_mapped(AltaReserva())
@autenticadoCli()
def crearReserva(data=None, auth=None):

    nReserva = Reserva()
    nReserva.fechaInicioReserva = data["inicio"]
    nReserva.fechaFinReserva = data["fin"]
    nReserva.habitacion_num = data["habitacion"]
    nReserva.usuario_id = auth.get('sub')
    
    if nReserva.fechaInicioReserva > nReserva.fechaFinReserva:
        return {"mensaje" : "La fecha de inicio debe ser menor a la fecha final de la reserva."}
    

        #[h for h in habitacion if ] comprehension
    dispo = Habitacion.query.filter(
        Habitacion.numeroHabitacion == nReserva.habitacion_num,
        Habitacion.disponible,
        ~Habitacion.reservas.any(
            (Reserva.fechaInicioReserva < nReserva.fechaFinReserva) &
            (Reserva.fechaFinReserva > nReserva.fechaInicioReserva)
        )
    ).first()
    
    if not dispo:
        return {"mensaje": "La habitación no está disponible en el rango de fechas solicitado."}, 400

    db.session.add(nReserva)
    db.session.commit()

    return {"mensaje": "Reserva creada con éxito"}
  
"""
    user_id = auth.get("sub")
    
    if not user_id:
        return {"error": "Usuario no autenticado"}, 401
      
    reserva= Reserva
    reserva.fechaInicioReserva=data['inicio']
    reserva.fechaFinReserva=data['fin']
    reserva.habitacion_num=data['habitacion']
    reserva.usuario_id = user_id
    
    db.session.add(reserva)
    db.session.commit()
    return {
           "mensaje": "reserva creada correctamente"
       }
"""






@reservas.route("/reservas", methods= ['GET'])
@autenticadoEmple()
def obtenerReserva(auth=None):

    reservas= Reserva.query.all()
    
    rSchema = ReservaSchema(exclude = ['habitacion','usuario','precioPorDia'], many=True)
    return rSchema.dump(reservas)


@reservas.route("/reservas/<int:id>", methods=['GET'])
@autenticadoEmple()
def obtenerReservaPorId(id):
    
    reservaId= Reserva.query.get(id)

    reservaSchema = ReservaSchema()
   
    reserva= reservaSchema.dump(reservaId)
   
    return {"status":200, "reserva":reserva}

 
    
@reservas.route("/habitaciones/disponibles", methods=['GET'])
@autenticadoCli()
def obtenerHabitacionesDisponibles(auth):
   
        fechaInicio = request.args.get('inicio')
        fechaFin = request.args.get('fin')
        
        try:
            fechaInicio = datetime.strptime(fechaInicio, '%d/%m/%Y').date()
            fechaFin = datetime.strptime(fechaFin, '%d/%m/%Y').date()
        except ValueError:
            return {"error": "Formato de fecha inválido. Usa DD/MM/YYYY."}, 400

        #[h for h in habitacion if ] comprehension
        dispo = [
            habitacion for habitacion in Habitacion.query.all()
            if habitacion.disponible and all(
                not (reserva.fechaInicioReserva < fechaFin and reserva.fechaFinReserva > fechaInicio)
                for reserva in habitacion.reservas
            ) 
        ]
        
        rSchema = ReservaSchemaHab(exclude = ['usuario'], many=True)
        return rSchema.dump(dispo)


@reservas.route("/reservas/disponible/<fecha>", methods=['GET'])
@autenticadoEmple()
def obtenerReservasPorFecha(fecha, auth=None):
    fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    disponibles = [
        habitacion for habitacion in Habitacion.query.all()
        if habitacion.disponible == True and all( 
            not (reserva.fechaInicioReserva <= fecha <= reserva.fechaFinReserva)
            for reserva in habitacion.reservas
        )
    ]

    
    noDisponibles = [
        habitacion for habitacion in Habitacion.query.all()
        if habitacion.disponible == False or any( 
            reserva.fechaInicioReserva <= fecha <= reserva.fechaFinReserva
            for reserva in habitacion.reservas
        )
    ]
    
    
    
    habitacionSchema = HabitacionSchema(many=True)
    disponiblesSerializadas = habitacionSchema.dump(disponibles)
    noDisponiblesSerializadas = habitacionSchema.dump(noDisponibles)

    return {
        "disponibles": disponiblesSerializadas,
        "noDisponibles": noDisponiblesSerializadas,
        "status": 200
    }



    
