from flask import Blueprint

mtagihan = Blueprint('mtagihan', __name__)

from . import views