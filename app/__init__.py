import logging
import random
from logging.handlers import RotatingFileHandler

import numpy
from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate


from config import Config
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, logger=False, engineio_logger=False)

if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/preformir.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)


from app import routes, errors, models, main

from app import db_init_seed

