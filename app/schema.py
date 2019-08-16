from . import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username','password_hash')


class ProdiSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nama_prodi', 'deleted_prodi')