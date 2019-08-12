from flask import Blueprint
from flask_restful import Api


mahasiswa = Blueprint('mahasiswa', __name__)
api_mhs = Api(mahasiswa)

from . import views