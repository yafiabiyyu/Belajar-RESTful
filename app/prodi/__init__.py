from flask import Blueprint

prodi = Blueprint('prodi', __name__)

from . import views