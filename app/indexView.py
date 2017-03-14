## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash
from services.services import errorMessage, successMessage
from markupsafe import escape

indexBP = Blueprint('indexBP', __name__)

# indexView
@indexBP.route('/')
def indexView():
    successMessage('hej')
    errorMessage('hej')
    return render_template('index.html')
