from flask import Blueprint

pembayaran = Blueprint('pembayaran', __name__)

from . import views