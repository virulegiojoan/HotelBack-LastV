from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .usuario import Usuario
from .habitacion import Habitacion
from .reserva import Reserva