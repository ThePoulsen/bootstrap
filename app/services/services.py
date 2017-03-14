## -*- coding: utf-8 -*-
from flask import flash

def errorMessage(msg):
    return flash(str(msg), ('danger', 'Error'))

def successMessage(msg):
    return flash(str(msg), ('success','Success'))
