## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for
from forms import loginForm, registerForm, setPasswordForm
from authAPI import authAPI
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, sendMail
import os

authBP = Blueprint('authBP', __name__)

# loginView
@authBP.route('/login', methods=['GET','POST'])
def loginView():
    form = loginForm()
    if 'token' in session:
        errorMessage('You are already logged in')
        return redirect(url_for('indexBP.indexView'))
    else:
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
    if 'token' in session:
        errorMessage('Please log out before registering a new account')
        return redirect(url_for('indexBP.indexView'))

    if form.validate_on_submit():
        dataDict = {'regNo' : form.regNo.data,
                    'companyName' : form.companyName.data,
                    'userName' : form.userName.data,
                    'email' : form.email.data,
                    'password' : form.password.data}
        req = authAPI('register', method='post', dataDict=dataDict)

        if 'error' in req:
            errorMessage(req['error'])

        elif 'success' in req:
            # send email confirmation
            subject = u'Please confirm your account'
            tok = req['token']
            email = req['email']
            confirm_url = url_for('authBP.confirmEmailView',token=tok, _external=True)
            html = render_template('email/verify.html', confirm_url=confirm_url)

            sendMail(subject=subject,
                     sender=os.environ['mailSender'],
                     recipients=[email],
                     html_body=html,
                     text_body = None)
            successMessage('You have successfully registered your account, please check your email for confirmation.')
            return redirect(url_for('indexBP.indexView'))

    return render_template('auth/register.html', form=form)

# setPasswordView
@authBP.route('/setPassword', methods=['GET','POST'])
def setPasswordView():
    form = setPasswordForm()
    if form.validate_on_submit():
        return 'hej'
    return render_template('auth/setPassword.html', form=form)

# confirmEmailView
@authBP.route('/confirm/<string:token>', methods=['GET'])
def confirmEmailView(token):
    if 'token' in session:
        errorMessage('Please log out before confirming a new account')
        return redirect(url_for('indexBP.indexView'))

    else:
        req = authAPI('confirm', method='post', token=token)
        if 'error' in req:
            errorMessage(req['error'])

        elif 'success' in req:
            if req['mustSetPass'] == 'True':
                successMessage('Your profile has been confirmed, please set your new password')
                return redirect(url_for('authBP.setPasswordView', tok=req['token']))
            else:
                successMessage('Your profile has been confirmed, please login')
                return redirect(url_for('authBP.loginView'))

    return redirect(url_for('indexView'))

# logoutView
@authBP.route('/logout', methods=['GET','POST'])
def logoutView():
    session.clear()
    successMessage(u'You are now logged out')
    return redirect(url_for('indexBP.indexView'))
