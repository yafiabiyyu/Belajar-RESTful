from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Pengguna(db.Model):

    __tablename__ = 'm_pengguna'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    deleted_pegawai = db.Column(db.Boolean, default=False)
    transaksi_tagihan = db.relationship('TransaksiTagihan', backref='tr_pengguna', lazy='dynamic')
    pembayaran_pegawai = db.relationship('Pembayaran', backref='pembayaran_pegawai', lazy='dynamic')

    def __repr__(self,id,username,password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @property
    def password(self):
        raise AttributeError('password is not areadable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Mahasiswa(db.Model):

    __tablename__ = 'm_mahasiswa'

    id = db.Column(db.Integer, primary_key=True)
    id_prodi = db.Column(db.Integer, db.ForeignKey('m_prodi.id'), nullable=False)
    nama = db.Column(db.String(50), unique=True)
    tahun_masuk = db.Column(db.Date)
    semester_mhs = db.Column(db.Integer, nullable=False)
    status_aktif = db.Column(db.Boolean, default=True)
    deleted_mhs = db.Column(db.Boolean, default=False)
    transaksi_tagihan = db.relationship('TransaksiTagihan', backref='tr_mahasiswa', lazy='dynamic')



class Prodi(db.Model):

    __tablename__ = 'm_prodi'

    id = db.Column(db.Integer, primary_key=True)
    nama_prodi = db.Column(db.String(20), nullable=False)
    deleted_prodi = db.Column(db.Boolean, default=False)
    mahasiswa_prodi = db.relationship('Mahasiswa', backref='mahasiswa_prodi', lazy='dynamic')


class JenisTagihan(db.Model):

    __tablename__ = 'jns_tagihan'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nama_jns_tagihan = db.Column(db.String(50), nullable=False, unique=True)
    deleted_jns_tagihan = db.Column(db.Boolean, default=False)
    master_tagihan = db.relationship('Tagihan', backref='jenis', lazy='dynamic')


class Tagihan(db.Model):

    __tablename__ = 'm_tagihan'

    id = db.Column(db.Integer, primary_key=True)
    id_jns_tagihan = db.Column(db.Integer, db.ForeignKey('jns_tagihan.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    deleted_tagihan = db.Column(db.Boolean, default=False)
    transaksi_tagihan = db.relationship('TransaksiTagihan', backref='transaksi_tagihan', lazy='dynamic')


class Pembayaran(db.Model):

    __tablename__ = 'tr_pembayaran'

    id = db.Column(db.Integer, primary_key=True)
    id_tr_tagihan = db.Column(db.Integer, db.ForeignKey('tr_tagihan.id'), nullable=False)
    id_pegawai = db.Column(db.Integer, db.ForeignKey('m_pengguna.id'), nullable=False)
    tgl_pembayaran = db.Column(db.Date)
    jumlah_bayar = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=False)
    deleted_tr_pembayaran =  db.Column(db.Boolean, default=False)


class TransaksiTagihan(db.Model):

    __tablename__ = 'tr_tagihan'

    id = db.Column(db.Integer, primary_key=True)
    id_tagihan = db.Column(db.Integer, db.ForeignKey('m_tagihan.id'), nullable=False)
    id_pegawai = db.Column(db.Integer, db.ForeignKey('m_pengguna.id'), nullable=False)
    id_mahasiswa = db.Column(db.Integer, db.ForeignKey('m_mahasiswa.id'), nullable=False)
    tgl_tagihan = db.Column(db.Date)
    jumlah_kurang = db.Column(db.Integer)
    deleted_tr_tagihan = db.Column(db.Boolean, default=False)
    pembayaran = db.relationship('Pembayaran', backref='pembayaran_tr', lazy='dynamic')


class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)




