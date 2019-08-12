from flask_restful import Resource
from flask import request
from . import api_mhs

class DataMhs(Resource):
    def get(self):
        return {'coba':'mahasiswa'}

    def post(self,nama,semester):
        nama = request.form.get('nama')
        semester = request.form.get('semester')
        return {'nama':nama,'semester':semester}

api_mhs.add_resource(DataMhs,'/mahasiswa/api/')