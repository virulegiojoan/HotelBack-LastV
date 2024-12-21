from functools import wraps
from config import Config

from flask import request
import jwt

#args = La lista de categorias que pueden usar la ruta
def autenticadoCli( *args ):

    def decorador(func_ruta):
        @wraps(func_ruta)
        def interna(*args,**kwargs):
            secreto = Config.SECRET_KEY
            tokenDelHead = request.headers.get("n-auth","")
            
            if not tokenDelHead:
                return {"error": "Token no encontrado en el encabezado 'n-auth'"}, 401
            
            if tokenDelHead.startswith("bearer "):
                token = tokenDelHead[7:]
            else:
                return {"error": "Formato de token inválido. Debe empezar con 'bearer '"}, 400
            
            try:
                # Decodificar el token
                auth = jwt.decode(token, secreto, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return {"error": "El token ha expirado."}, 401
            except jwt.InvalidTokenError:
                return {"error": "Token inválido."}, 401
            
            if auth.get("tipoUsuario") != "CLIENTE":
                return {"error": "Permiso denegado"}, 403
            auth['sub'] = auth['id']
            return func_ruta(*args,**kwargs,auth=auth)
        return interna
    
    return decorador

def autenticadoEmple( *args ):

    def decorador(func_ruta):
        @wraps(func_ruta)
        def interna(*args,**kwargs):
            secreto = Config.SECRET_KEY
            tokenDelHead = request.headers.get("n-auth","")
            
            if not tokenDelHead:
                return {"error": "Token no encontrado en el encabezado 'n-auth'"}, 401
            
            if tokenDelHead.startswith("bearer "):
                token = tokenDelHead[7:]
            else:
                return {"error": "Formato de token inválido. Debe empezar con 'bearer '"}, 400
            
            try:
                # Decodificar el token
                auth = jwt.decode(token, secreto, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return {"error": "El token ha expirado."}, 401
            except jwt.InvalidTokenError:
                return {"error": "Token inválido."}, 401
            
            if auth.get("tipoUsuario") != "EMPLEADO":
                return {"error": "Permiso denegado"}, 403
            auth['sub'] = auth['id']
            return func_ruta(*args,**kwargs,auth=auth)
        return interna
    
    return decorador

def json_mapped(esquema):

    def decorador(funcion_ruta):
        @wraps(funcion_ruta)
        def interna(*args,**kwargs):
            datos = esquema.load( request.json)
            return funcion_ruta(*args,**kwargs,data=datos)
        return interna
    
    return decorador

