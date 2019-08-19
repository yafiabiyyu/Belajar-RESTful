from flask_restful import Resource, reqparse, inputs
from flask import jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime


#local import
from . import api_mhs
from ..models import Mahasiswa
from .. import db


#requestparser setup
parser = reqparse.RequestParser()
parser.add_argument('nama', type=str, help='Nama mahasiswa harus di isi', required=True)
parser.add_argument('tahun_masuk',type=inputs.date, help='Tahun masuk harus di isi', required=True)
parser.add_argument('semester_mhs', type=int, help='Tahun semester wajib di isi', required=True)
parser.add_argument('status_aktif', type=bool, help='Status aktfi harus di isi', required=True)
parser.add_argument('deleted_mhs', type=bool, help='Deleted harus di hapus', required=True)
parser.add_argument('id_prodi',type=int, help='Id prodi harus di isi', required=True)


class DataMahasiswa(Resource):
    def post(self):
        data = parser.parse_args()
        check_mahasiswa = Mahasiswa.query.filter_by(nama=data['nama']).first()
        data_tanggal = data['tahun_masuk']
        tanggal = datetime.strftime(data_tanggal, '%Y-%m-%d')
        if check_mahasiswa is None:
            mahasiswa = Mahasiswa(
              id_prodi=data['id_prodi'],
              nama=data['nama'],
              tahun_masuk= tanggal,
              semester_mhs=data['semester_mhs'],
              status_aktif=data['status_aktif'],
              deleted_mhs=data['deleted_mhs'],
            )
            db.session.add(mahasiswa)
            db.session.commit()
            return {'message':'Data berhasil di tambahkan'}
        else:
            return {'message':'Data gagal ditambahkan'}

api_mhs.add_resource(DataMahasiswa, '/mahasiswa/api/data/')


