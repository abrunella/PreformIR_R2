from flask import render_template, jsonify

from app import app, socketio
from app.models import Setting, Alert_Log, Sensor, Reading_Temperature


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    alarm_setting = Setting.query.filter_by(name='ALARM_THRESHOLD').first()
    warning_setting = Setting.query.filter_by(name='WARNING_THRESHOLD').first()
    thresholds = {
        'warning': warning_setting.value,
        'alarm': alarm_setting.value
    }
    alert_log = Alert_Log.query.order_by(Alert_Log.timestamp_triggered).limit(5000).all()
    sensors = Sensor.query.filter(Sensor.isEnabled == 1).all()
    return render_template('index.html', thresholds=thresholds, alert_log=alert_log, sensors=sensors)

@app.route('/log')
@app.route('/log.html')
def log():
    sensor_log = Sensor.query.all()
    temperature_log = Reading_Temperature.query.filter(Reading_Temperature.sensor_id == 99).limit(500).all()
    temp_max = max(d.value_max for d in temperature_log)
    temp_min = min(d.value_min for d in temperature_log)
    temp_avg = sum(d.value_avg for d in temperature_log)/(len(temperature_log))
    print("Max: {max}, Min: {min}, Avg: {avg}".format(max=temp_max, min=temp_min, avg=temp_avg))
    temp_log_stats = {
        "Max": temp_max,
        "Min": temp_min,
        "Avg": temp_avg
    }

    return render_template('log.html', sensor_log=sensor_log, temperature_log=temperature_log,
                           temp_log_stats=temp_log_stats)

@app.route('/update_alarm_table', methods=['POST'])
def update_alarm_table():
    alert_log = Alert_Log.query.order_by(Alert_Log.timestamp_triggered).limit(5000).all()
    return jsonify({'text': 'test'})

@app.route('/setup')
@app.route('/setup.html')
def setup():
    return render_template('setup.html')

@socketio.on('connect')
def connect():
    print("A client just connected")