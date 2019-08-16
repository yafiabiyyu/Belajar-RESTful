# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow


# local import
from config import app_config


# db variable initialization
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config.setdefault('JWT_TOKEN_LOCATION',('headers', 'cookies'))
    migrate = Migrate(app,db)
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    from app import models

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(dec_token):
        jti = dec_token['jti']
        return models.RevokedToken.is_jti_blacklisted(jti)

    from .jenistagihan import jenistagihan as jenistagihan_blueprint
    app.register_blueprint(jenistagihan_blueprint)

    from .mahasiswa import mahasiswa as mahasiswa_blueprint
    app.register_blueprint(mahasiswa_blueprint)

    from .mtagihan import mtagihan as mtagihan_blueprint
    app.register_blueprint(mtagihan_blueprint)

    from .pembayaran import pembayaran as pembayaran_blueprint
    app.register_blueprint(pembayaran_blueprint)

    from .pengguna import pengguna as pengguna_blueprint
    app.register_blueprint(pengguna_blueprint)

    from .prodi import prodi as prodi_blueprint
    app.register_blueprint(prodi_blueprint)

    from .trtagihan import trtagihan as trtagihan_blueprint
    app.register_blueprint(trtagihan_blueprint)

    return app
