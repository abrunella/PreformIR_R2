from datetime import datetime

from app import db
from app.models import Setting, Alert_Log, Sensor, Reading_Temperature

# Settings
db.session.query(Setting).delete()
if not Setting.query.filter_by(name='ALARM_THRESHOLD').first():
    appset = Setting(name='ALARM_THRESHOLD', value=125)
    appset.type = "SETTING"
    db.session.add(appset)
    db.session.commit()
if not Setting.query.filter_by(name='WARNING_THRESHOLD').first():
    appset = Setting(name='WARNING_THRESHOLD', value=115)
    appset.type = "SETTING"
    db.session.add(appset)
    db.session.commit()
if not Setting.query.filter_by(name='RELAY_1_TYPE').first():
    appset = Setting(name='RELAY_1_TYPE', value='latched', type='RELAY_1')
    db.session.add(appset)
    appset = Setting(name='RELAY_1_DELAY', value=500, type='RELAY_1')
    db.session.add(appset)
    appset = Setting(name='RELAY_1_PIN', value=26, type='RELAY_1')
    db.session.add(appset)
    appset = Setting(name='RELAY_2_TYPE', value='momentary', type='RELAY_2')
    db.session.add(appset)
    appset = Setting(name='RELAY_2_DELAY', value=1000, type='RELAY_2')
    db.session.add(appset)
    appset = Setting(name='RELAY_2_PIN', value=20, type='RELAY_2')
    db.session.add(appset)
    appset = Setting(name='RELAY_3_TYPE', value='latched', type='RELAY_3')
    db.session.add(appset)
    appset = Setting(name='RELAY_3_DELAY', value=500, type='RELAY_3')
    db.session.add(appset)
    appset = Setting(name='RELAY_3_PIN', value=21, type='RELAY_3')
    db.session.add(appset)
    db.session.commit()

# Alert Log
#db.session.query(Alert_Log).delete()

#Temperature Log
#db.session.query(Reading_Temperature).delete()

# Sensor
db.session.query(Sensor).delete()
if not Sensor.query.filter_by(id=1).first():
    sen = Sensor(model='AMG8833', address=69, i2c_channel=0, isEnabled=1, isConnected=0)
    db.session.add(sen)
    sen = Sensor(model='TCS34725', address=70, i2c_channel=1, isEnabled=0, isConnected=0)
    db.session.add(sen)
    sen = Sensor(model='BREAKOUT', address=69, i2c_channel=2, isEnabled=0, isConnected=0)
    db.session.add(sen)
    sen = Sensor(model='AMG8833', address=69, i2c_channel=3, isEnabled=1, isConnected=0)
    db.session.add(sen)
    sen = Sensor(model='AMG8833', address=69, i2c_channel=4, isEnabled=1, isConnected=0)
    db.session.add(sen)
    sen = Sensor(model='BREAKOUT', address=69, i2c_channel=5, isEnabled=0, isConnected=0)
    db.session.add(sen)
    sen = Sensor(model='TCS34725', address=70, i2c_channel=6, isEnabled=0, isConnected=0)
    db.session.add(sen)
    sen = Sensor(model='AMG8833', address=69, i2c_channel=7, isEnabled=1, isConnected=0)
    db.session.add(sen)
    db.session.commit()

db.session.query()
