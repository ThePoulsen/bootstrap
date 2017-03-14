## -*- coding: utf-8 -*-
from flask import flash, session, redirect, url_for
from app import db
from functools import wraps
from authAPI import authAPI

def errorMessage(msg):
    return flash(str(msg), ('danger', 'Error'))

def successMessage(msg):
    return flash(str(msg), ('success','Success'))

def listData(model, **kwargs):
    data = model.query.all()
    return data

# flask view decorators
def requiredRole(*roleList):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not 'token' in session:
                errorMessage('You are required to log into your account to view this content')
                return redirect(url_for('authBP.loginView'))
            if not 'roles' in session:
                roles = []
            else:
                roles = session['roles']
            if not any([i in roleList[0] for i in roles]):
                errorMessage('You are not authorized to access this content')
                return redirect(url_for('indexBP.indexView'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def loginRequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'token' in session:
            errorMessage('You are required to log into your account to view this content')
            return redirect(url_for('authBP.loginView'))
        req = authAPI(endpoint='checkPassword', method='post', token=session['token'])
        if 'error' in req:
            errorMessage('You are required to log into your account to view this content')
            return redirect(url_for('authBP.loginView'))
        return f(*args, **kwargs)
    return decorated_function
