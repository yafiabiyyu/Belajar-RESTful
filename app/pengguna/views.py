from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import (create_access_token,create_refresh_token,
                                jwt_required,jwt_refresh_token_required,
                                get_jwt_identity,get_raw_jwt)
from . import api_pengguna
from ..models import Pengguna, RevokedToken
from .. import db,jwt,models
from ..schema import UserSchema

users_schema = UserSchema()
user_schema = UserSchema(many=True)



parser = reqparse.RequestParser()
parser.add_argument('username', help='username tidak boleh kosong', required= True)
parser.add_argument('password', help='password tidak boleh kosong', required= True)


class PenggunaRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        check_user = Pengguna.query.filter_by(username=data['username']).first()
        if check_user is None:
            penggguna = Pengguna(
                username=data['username'],
                password=data['password']
            )
            db.session.add(penggguna)
            db.session.commit()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message':'User {} berhasil di buat'.format(data['username']),
                'access_token':access_token,
                'refresh_token':refresh_token
            }
        else:
            return {'message': 'User sudah terdaftar'}



class PenggunaLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = Pengguna.query.filter_by(username=data['username']).first()
        if current_user is not None and current_user.verify_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} berhasil login'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message':'Wrong credentials'}





class PenggunaLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message':'Token berhasil di hapus'}
        except:
            return {'message': 'Terjadi kesalahan'}, 500




class PenggunaLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message': 'Token refresh berhasil di hapus'}
        except:
            return {'message': 'Terjadi kesalahan'}, 500



class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        currnet_user = get_jwt_identity()
        access_token = create_access_token(currnet_user)
        return {'access_token':access_token}


class ListPengguna(Resource):
    @jwt_required
    def get(self):
        data_pegawai = Pengguna.query.all()
        result = user_schema.dump(data_pegawai)
        return jsonify(result.data)



class DataPengguna(Resource):
    @jwt_required
    def get(self,id):
        data_pegawai = Pengguna.query.get(id)
        return users_schema.jsonify(data_pegawai)

    @jwt_required
    def put(self,id):
        data = parser.parse_args()
        pegawai = Pengguna.query.filter_by(id=id).first()
        if pegawai is None:
            return {'message':'Data pegawai tidak ditemukan'}
        else:
            pegawai.username = data['username']
            pegawai.password = data['password']
            db.session.commit()
            return users_schema.jsonify(pegawai)

    @jwt_required
    def delete(self,id):
        pegawai = Pengguna.query.filter_by(id=id).first()
        if pegawai is None:
            return {'message':'Data pegawai tidak ditemukan'}
        else:
            db.session.delete(pegawai)
            db.session.commit()
            return users_schema.jsonify(pegawai)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(dec_token):
    jti = dec_token['jti']
    return models.RevokedToken.is_jti_blacklisted(jti)



#endpoint setup
api_pengguna.add_resource(PenggunaRegistration,'/pengguna/api/registration/')
api_pengguna.add_resource(PenggunaLogin,'/api/login/')
api_pengguna.add_resource(PenggunaLogout,'/api/logout/')
api_pengguna.add_resource(PenggunaLogoutRefresh, '/pengguna/api/logout/refresh/')
api_pengguna.add_resource(TokenRefresh, '/pengguna/api/token/refresh/')
api_pengguna.add_resource(ListPengguna,'/pengguna/api/data/pengguna/')
api_pengguna.add_resource(DataPengguna, '/pengguna/api/data/detail/pengguna/<int:id>/')