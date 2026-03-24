from flask import Blueprint

# DEFINIMOS EL BLUEPRINT
auth = Blueprint('auth', __name__)

# IMPORTAMOS LAS RUTAS
from . import routes