import adafruit_amg88xx
import numpy as np

from app import db
from datetime import datetime

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    value = db.Column(db.String(256), nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'last_modified': self.last_modified.isoformat() + 'Z'
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'value']:
            if field in data:
                setattr(self, field, data[field])

    def update_setting(self, value):
        setting = self.query.filter_by(name=self.name).first()
        setting.value = value
        setting.last_modified = datetime.utcnow()
        db.session.commit()
        return value

class Sensor(db.Model):

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Sensor
    model = db.Column(db.String(32), nullable=False)
    address = db.Column(db.Integer)
    i2c_channel = db.Column(db.Integer)
    isEnabled = db.Column(db.Integer)
    isConnected = db.Column(db.Integer)
    last_update = db.Column(db.DateTime)

    # Relationships
    temp_readings = db.relationship('Reading_Temperature', backref='sensor', lazy=True)

    def __init__(self, **kwargs):
        # Helps with class initiation, basically what ever attribute you give
        # at initiation will become a class attribute with this __init__ method
        super(Sensor, self).__init__(**kwargs)


    def get_readings(self):
        """
            Get sensor readings.

            Get the sensors readings, store in the database, and return a collection
            containing the information.

            Parameters:
            self (Sensor): self

            Returns:
            Reading_Temperature: See models/reading_temperature.py

        """
        pass

class Reading_Temperature(db.Model):
    __tablename__ = 'reading_temperature'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    value_min = db.Column(db.Float, index=True, nullable=False)
    value_max = db.Column(db.Float, index=True, nullable=False)
    value_avg = db.Column(db.Float, index=True, nullable=True)
    pixel_array = db.Column(db.PickleType)

    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    message = db.Column(db.String(256), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    logType_id = db.Column(db.Integer, db.ForeignKey('logType.id'))
    logLevel_id = db.Column(db.Integer, db.ForeignKey('logLevel.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.setting + self.value)


class Log_Type(db.Model):
    __tablename__ = 'logType'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, index=True, nullable=False)

    logs = db.relationship('Log', backref='type', lazy=True)


class Log_Level(db.Model):
    __tablename__ = 'logLevel'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String, index=True, nullable=False)

    logs = db.relationship('Log', backref='level', lazy=True)

class Alert_Log(db.Model):
    __tablename__ = 'alert_log'
    id = db.Column(db.Integer, primary_key=True)
    timestamp_triggered = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    threshold = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.String, index=True)
    timestamp_cleared = db.Column(db.DateTime, index=True)

    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    history = db.relationship('Log', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_login': self.last_login.isoformat() + 'Z'
        }
        if include_email:
            data['email'] = self.email
        return data

    # TODO: Fix this method to return better data
    def to_collection_dict(self):
        resources = self.query.order_by(self.username).all()
        data = {
            'items': [item.to_dict() for item in resources]
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class AMG8833(adafruit_amg88xx.AMG88XX):
    def __init__(self, i2c, device_id):
        super().__init__(i2c)
        self.Id = device_id

    def pixels_f(self):
        a = np.array(super().pixels)
        f = (a * 9 / 5 + 32)
        return f.round(1)
