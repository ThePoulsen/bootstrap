## -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import flask_sijax
from flask_htmlmin import HTMLMIN
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *


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

nav = Nav()
nav.init_app(app)

# registers the "top" menubar
topbar = Navbar('',
    View('Home', 'indexBP.indexView'),
    View('Home', 'indexBP.indexView'),
)
nav.register_element('top', topbar)


# Import models
#from app.api.models import *

## import blueprints
from .indexView import indexBP

## Register blueprints
app.register_blueprint(indexBP, url_prefix='')
