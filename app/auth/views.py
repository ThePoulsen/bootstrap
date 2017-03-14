## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request
from forms import loginForm, registerForm, setPasswordForm
from authAPI import authAPI

authBP = Blueprint('authBP', __name__)

# loginView
@authBP.route('/login', methods=['GET','POST'])
def loginView():
    form = loginForm()
    if form.validate_on_submit():
        return 'hej'
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
