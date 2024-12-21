from flask import Blueprint
from app import db

inicializarSql =Blueprint('inicializar', __name__)

@inicializarSql.route("/init")
def init():
    db.create_all()
    return "ok"
    
