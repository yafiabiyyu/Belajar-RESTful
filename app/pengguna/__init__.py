from flask import Blueprint
from flask_restful import Api

pengguna = Blueprint('pengguna', __name__)
api_pengguna = Api(pengguna)

from . import views