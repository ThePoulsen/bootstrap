## -*- coding: utf-8 -*-
from flask import flash

def errorMessage(msg):
    return flash(str(msg), 'error')

def successMessage(msg):
    return flash(str(msg), 'success')
