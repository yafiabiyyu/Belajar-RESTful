from flask import Blueprint
from flask_restful import Api

prodi = Blueprint('prodi', __name__)
api_prodi = Api(prodi)

from . import views