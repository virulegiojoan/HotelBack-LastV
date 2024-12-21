from flask import Flask
from models import db
from schemas import ma
from routes.usuariosRoutes import usuarios
from routes.habitacionesRoutes import habitaciones
from routes.inicializarSqlRoute import inicializarSql
from routes.reservaRoutes import reservas
from routes.loginRoute import Login
from config import Config
from extensions import bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
bcrypt.init_app(app)

db.init_app(app)
ma.init_app(app)

app.register_blueprint(usuarios)
app.register_blueprint(habitaciones)
app.register_blueprint(inicializarSql)
app.register_blueprint(reservas)
app.register_blueprint(Login)