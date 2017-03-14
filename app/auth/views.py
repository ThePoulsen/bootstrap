## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for
from forms import loginForm, registerForm, setPasswordForm
from authAPI import authAPI
from app.services.services import errorMessage, successMessage

authBP = Blueprint('authBP', __name__)

# loginView
@authBP.route('/login', methods=['GET','POST'])
def loginView():
    form = loginForm()
    if form.validate_on_submit():
        dataDict = {'regNo':form.regNo.data,
                    'email':form.email.data,
                    'password':form.password.data}

        req = authAPI('login', method='post', dataDict=dataDict)

        if 'success' in req:
            session['token'] = req['token']
            session['email'] = req['email']
            session['roles'] = req['roles']
            session['tenant_uuid'] = req['tenant_uuid']
            session['user_uuid'] = req['user_uuid']
            successMessage('You are now logged in')
            return redirect(url_for('indexBP.indexView'))

        elif u'error' in req:
            if req['error'] == 'Could not identify Tenant':
                    errorMessage('We are not able to validate your credentials')

            elif req['error'] == 'Could not identify User':
                errorMessage('We are not able to validate your credentials')

            elif req['error'] == 'Wrong user/password combination':
                errorMessage(req['error']+' - Attempts left: '+req['attempts left'])

            else:
                errorMessage(unicode(req))


    return render_template('auth/login.html', form=form)

# registerView
@authBP.route('/register', methods=['GET','POST'])
def registerView():
    form = registerForm()
    if form.validate_on_submit():
        return 'hej'
    return render_template('auth/register.html', form=form)

# setPasswordView
@authBP.route('/setPassword', methods=['GET','POST'])
def setPasswordView():
    form = setPasswordForm()
    if form.validate_on_submit():
        return 'hej'
    return render_template('auth/setPassword.html', form=form)

# logoutView
@authBP.route('/logout', methods=['GET','POST'])
def logoutView():
    session.clear()
    successMessage(u'You are now logged out')
    return redirect(url_for('indexBP.indexView'))
