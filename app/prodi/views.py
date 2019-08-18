from flask import jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required

#local import
from . import api_prodi
from ..models import Prodi
from .. import db
from ..schema import ProdiSchema


#prodi argument
parser = reqparse.RequestParser()
parser.add_argument('nama_prodi', help='nama prodi tidak boleh kosong', required=True)
parser.add_argument('deleted_prodi', type=bool)

#Prodi Schema
prodi_schema = ProdiSchema(many=True)
prodischema = ProdiSchema()


class ListProdi(Resource):
    @jwt_required
    def get(self):
        data = Prodi.query.all()
        if data is not None:
            result = prodi_schema.dump(data)
            return jsonify(result.data)
        else:
            return {'message':'Data tidak ditemukan'}

    def post(self):
        prodi_argument = parser.parse_args()
        check_prodi = Prodi.query.filter_by(nama_prodi=prodi_argument['nama_prodi']).first()
        if check_prodi is None:
            prodi = Prodi(
                nama_prodi=prodi_argument['nama_prodi'],
            )
            db.session.add(prodi)
            db.session.commit()
            return {'message':'Data berhasil disimpan'}
        else:
            return {'message':'Data gagal disimpan'}


class DataProdi(Resource):
    @jwt_required
    def get(self,id):
        data_prodi = Prodi.query.get(id)
        if data_prodi is None:
            return {'message':'Data tidak ditemukan'}
        else:
            return prodischema.jsonify(data_prodi)
    @jwt_required
    def put(self,id):
        data = parser.parse_args()
        prodi = Prodi.query.filter_by(id=id).first()
        if prodi is None:
            return {'message':'Data tidak ditemukan'}
        else:
            prodi.nama_prodi = data['nama_prodi']
            prodi.deleted_prodi = data['deleted_prodi']
            db.session.commit()
            return prodischema.jsonify(prodi)
    @jwt_required
    def delete(self,id):
        prodi = Prodi.query.filter_by(id=id).first()
        if prodi is None:
            return {'message':'Data tidak ditemukan'}
        else:
            db.session.delete(prodi)
            db.session.commit()
            return prodischema.jsonify(prodi)


api_prodi.add_resource(ListProdi, '/prodi/api/data/')
api_prodi.add_resource(DataProdi, '/prodi/api/data/detail/<int:id>/')