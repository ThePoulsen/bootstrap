## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash
from markupsafe import escape

indexBP = Blueprint('indexBP', __name__)

# indexView
@indexBP.route('/')
def indexView():
    flash('hej')
    return render_template('index.html')

# indexView
@indexBP.route('/test')
def davView():
    return render_template('dav.html')
