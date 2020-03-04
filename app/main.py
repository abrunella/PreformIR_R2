import random
from json import dumps

import eventlet

from app import db, socketio
from app.models import Reading_Temperature, Setting, Alert_Log, Sensor, AMG8833

eventlet.monkey_patch()

from datetime import datetime
import numpy as np

import board
import busio
import RPi.GPIO as GPIO
from adafruit_tca9548a import TCA9548A

# Create the I2C Bus for the RaspberryPi
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A multiplexer object and give it the I2C bus.
tca_i2c_multiplexer = TCA9548A(i2c_bus)

# Setup the GPIO pins for the relay outputs.
# Set BCM GPIO numbering
GPIO.setmode(GPIO.BCM)
# Set pins as outputs
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

sensor_db = Sensor.query.filter(Sensor.model == 'AMG8833', Sensor.isEnabled == 1).all()
sensors = []

for i in sensor_db:
    try:
        sensors.append(AMG8833(tca_i2c_multiplexer[i.i2c_channel], i.id))
    except ValueError as arg:
        print("Failed to communicate with sensor {num} @ channel->{ch}. Exception: {arg}".format(num=i.id,
                                                                                                 ch=i.i2c_channel,
                                                                                                 arg=arg))
        # Set the sensor status to disconnected
        i.isConnected = 0
        i.isEnabled = 0
        db.session.commit()

print(sensors)


def get_temperature_readings(simulate=False):
    # print("Sensor Reading: {sen}".format(sen=sen.get_readings()))
    pix_all = []
    # print("Get Readings...")
    # Get all the pixel readings from all the AMGs
    for temp_sensor in sensors:
        if simulate:
            pix = np.random.randint(60, 90, 2)
        else:
            sen_update = Sensor.query.filter_by(id=temp_sensor.Id).first()
            try:
                pix = np.array(temp_sensor.pixels_f())
                sen_update.isConnected = 1
                sen_update.last_update = datetime.utcnow()
                db.session.commit()
            except OSError as arg:
                print("Failed to communicate with sensor {num} @ channel->{ch}. Exception: {arg}".format(
                    num=temp_sensor.Id, ch=temp_sensor.i2c_device.i2c, arg=arg))
                sen_update.isConnected = 0
                db.session.commit()
                continue

        # Get minimum, maximum, mean, median
        maxread = round(np.amax(pix), 2)
        minread = round(np.amin(pix), 2)
        avgread = round(np.mean(pix), 2)

        reading = Reading_Temperature(
            value_min=minread,
            value_max=maxread,
            value_avg=avgread,
            pixel_array=pix,
            sensor_id=temp_sensor.Id
        )

        db.session.add(reading)

        data = {
            'sensor': temp_sensor.Id,
            'max': float(reading.value_max),
            'min': float(reading.value_min),
            'avg': float(reading.value_avg),
            'timestamp': datetime.utcnow.__str__()
        }
        socketio.emit('status-sensor-temperatures', data)
        pix_all.append(pix)

    maxreading = np.amax(pix_all)
    minreading = np.amin(pix_all)
    avgreading = np.average(pix_all)
    data = {
        'max': round(float(maxreading), 1),
        'min': round(float(minreading), 1),
        'avg': round(float(avgreading), 1)
    }
    socketio.emit('status-overall-temperatures', data)
    reading = Reading_Temperature(
        value_min=minreading,
        value_max=maxreading,
        value_avg=avgreading,
        sensor_id=99
    )
    db.session.add(reading)
    db.session.commit()
    # Check for warnings
    warning_threshold = Setting.query.filter_by(name='WARNING_THRESHOLD').first()
    warning_threshold = warning_threshold.value
    if (float(maxreading) >= int(warning_threshold)):
        alert_log = Alert_Log(
            threshold=warning_threshold,
            value=maxreading,
            type='Warning',
            sensor_id=random.randint(1, 4),
            timestamp_cleared=datetime.utcnow()
        )
        db.session.add(alert_log)

    # Check for alarms
    # First make sure no alarms are already set.
    alarm_active = Alert_Log.query.filter(Alert_Log.timestamp_cleared == None, Alert_Log.type == 'Alarm').first()
    warning_active = Alert_Log.query.filter(Alert_Log.timestamp_cleared == None, Alert_Log.type == 'Warning').first()

    if (alarm_active is None):
        alarm_threshold = Setting.query.filter_by(name='ALARM_THRESHOLD').first()

        alarm_threshold = alarm_threshold.value

        if float(maxreading) >= int(alarm_threshold):
            alert_log = Alert_Log(
                threshold=alarm_threshold,
                value=maxreading,
                type='Alarm',
                sensor_id=random.randint(1, 4)
            )
            db.session.add(alert_log)
    else:
        # Alarm is set. Warning is always set to 0 so we need to change that.
        print("Alarm is set")
        print(alarm_active.type)
        alarm_status = {
            "active": 1,
            "value": alarm_active.value,
            "threshold": alarm_active.threshold,
            "timestamp": alarm_active.timestamp_triggered.isoformat()
        }
        socketio.emit('alarm-active-status', alarm_status)

    db.session.commit()


def get_readings_thread():
    while True:
        get_temperature_readings()

        eventlet.sleep(.5)


@socketio.on('btn-reset-alarm')
def btn_reset_alarm():
    alarm_active = Alert_Log.query.filter(Alert_Log.timestamp_cleared == None, Alert_Log.type == 'Alarm').first()
    if (alarm_active is not None):
        print("Reseting Alarm!!!")
        alarm_active.timestamp_cleared = datetime.utcnow()
        db.session.commit()


@socketio.on('btn-click-high-temp-thresholds')
def btn_high_temp_thresholds(button, direction):
    print('btn-high-temp-thresholds -> {btn}, {dir}'.format(btn=button, dir=direction))
    try:
        alarm_setting = Setting.query.filter_by(name='ALARM_THRESHOLD').first()
        warning_setting = Setting.query.filter_by(name='WARNING_THRESHOLD').first()

        if (button == 'alarm'):
            value = int(alarm_setting.value)
            if (direction == 'up'):
                value += 1
            if (direction == 'dn'):
                value -= 1
            alarm_setting.update_setting(value=value)
        if (button == 'warning'):
            value = int(warning_setting.value)
            if (direction == 'up'):
                value += 1
            if (direction == 'dn'):
                value -= 1
            warning_setting.update_setting(value=value)
        data = {
            'warning': warning_setting.value,
            'alarm': alarm_setting.value
        }
        socketio.emit('setting-thresholds', data)
    except:
        print("Unable to change temperature!")


eventlet.spawn(get_readings_thread)
