from flask_marshmallow import Marshmallow

ma = Marshmallow()

from .schemas import UsuarioSchema
from .schemas import HabitacionSchema
from .schemas import ReservaSchema

from .requestSchema import AltaUser
from .requestSchema import AltaHabitacion
from .requestSchema import AltaReserva
from .requestSchema import EditarPrecio
from .requestSchema import LoginUser
