## -*- coding: utf-8 -*-
from flask import flash, session, redirect, url_for
from app import db, mail
from functools import wraps
from authAPI import authAPI
from flask_mail import Message
from wtforms import widgets, validators, DecimalField
from sqlalchemy import inspect

def compareDict(row, data):
    row = objectAsDict(row)
    d1_keys = set(row.keys())
    d2_keys = set(data.keys())
    intersect_keys = d1_keys.intersection(d2_keys)

    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (row[o], data[o]) for o in intersect_keys if row[o] != data[o]}
    same = set(o for o in intersect_keys if row[o] == data[o])
    return {'added':added, 'removed':removed, 'modified':modified, 'same':same}

def objectAsDict(obj):
    excludeList = ['_password','platform_uuid','tenant_uuid','id']
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs if not c.key in excludeList}

def errorMessage(msg):
    return flash(str(msg), ('danger', 'Error'))

def successMessage(msg):
    return flash(str(msg), ('success','Success'))

def listData(model, **kwargs):
    data = model.query.all()
    return data

def getUser(uuid):
    return authAPI(endpoint='user/'+unicode(uuid), method='get', token=session['token'])

def getRole(role):
    return authAPI(endpoint='getRole/'+unicode(role), method='get', token=session['token'])

# SendMail
def sendMail(subject, sender, recipients, text_body, html_body):
    mesg = Message(subject, sender=sender, recipients=recipients)
    mesg.body = text_body
    mesg.html = html_body
    mail.send(mesg)

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

# Select2 widget
class select2Widget(widgets.Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(select2Widget, self).__call__(field, **kwargs)

# Select2 multiple widget
class select2MultipleWidget(widgets.Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')
        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super(select2MultipleWidget, self).__call__(field, multiple = True, **kwargs)
