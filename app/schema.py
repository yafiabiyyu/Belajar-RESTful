from . import ma
from .models import Pengguna


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','username','password_hash')