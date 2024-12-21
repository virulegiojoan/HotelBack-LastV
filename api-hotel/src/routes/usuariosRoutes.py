from flask import Blueprint, request, jsonify
from schemas import UsuarioSchema
from app import db
from models.usuario import Usuario
from extensions import bcrypt
from schemas import AltaUser
from decorators.route_decorators import json_mapped

usuarios = Blueprint('usuarios', __name__)

@usuarios.route("/registro", methods=['POST'])
@json_mapped(AltaUser())
def crearUsuario(data=None):
    if data['clave1'] != data['clave2']:
        return {
            "mensaje": "Las claves no coinciden"
        }

    usuario= Usuario()
    usuario.email= data['usuario']
    usuario.clave=  bcrypt.generate_password_hash(data['clave1']).decode('utf-8')
    usuario.categoria= data['categoria'].upper()


    db.session.add(usuario)
    db.session.commit()

    return {
        "mensaje": "usuario creado correctamente"
    }

    


