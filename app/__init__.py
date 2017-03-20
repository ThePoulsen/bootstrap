## -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import flask_sijax
from flask_htmlmin import HTMLMIN
from flask_bootstrap import Bootstrap

# Setup Flask and read config from ConfigClass defined above
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Flask-SQLAlchemy
db = SQLAlchemy(app)

# Flask-mail
mail = Mail(app)

# HTML min
HTMLMIN(app)

# Flask-sijax
flask_sijax.Sijax(app)

# Flask-bootstrap
Bootstrap(app)

# Import models
from app.masterData.models import *
from app.user.models import *

## import blueprints
from .indexView import indexBP
from app.auth.views import authBP
from app.user.views import userBP
from app.masterData.views import mdBP

## Register blueprints
app.register_blueprint(indexBP, url_prefix='')
app.register_blueprint(authBP, url_prefix='')
app.register_blueprint(userBP, url_prefix='')
app.register_blueprint(mdBP, url_prefix='/masterData')
