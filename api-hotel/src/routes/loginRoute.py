from flask import Blueprint
import jwt
from app import db
from models import Usuario
from flask import request
import datetime
from extensions import bcrypt 
from config import Config
from decorators.route_decorators import json_mapped
from schemas import LoginUser

Login =Blueprint('login', __name__)


@Login.route("/login", methods=['POST'])
@json_mapped(LoginUser())
def login(data=None):
    data = request.json
    usuario = data['usuario']  
    clave = data['clave']  

    usuario = Usuario.query.filter_by(usuario=usuario).first()

    if usuario and bcrypt.check_password_hash(usuario.clave, clave):
         payload = {
            'id': usuario.id,  
            'tipoUsuario': usuario.categoria.name,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)  
        }
         
         token = jwt.encode(payload, Config.SECRET_KEY, 'HS256')
         
         return {
            "token": token,
            "categoria": usuario.categoria.name

            }
    else:
        return {
            "status": 401,

            
            "message": "Email o contraseña incorrectos"
        }



   
  