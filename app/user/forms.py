## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, BooleanField, RadioField, SelectMultipleField
from wtforms.validators import InputRequired, Email
from app.services.services import select2MultipleWidget

class userForm(FlaskForm):
    name = StringField('User name',[InputRequired('Please enter a user name')])
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    phone = StringField('Phone number')
    locked = RadioField('User locked?', choices=[('Locked','Locked'),('Unlocked','Unlocked')])
    role = RadioField('User role', choices=[('Administrator','Administrator'),('Superuser','Superuser'),('User','User')], validators=[InputRequired('Please select a user Role')])
    groups = SelectMultipleField('Groups', validators=[], choices=[], widget=select2MultipleWidget())

class groupForm(FlaskForm):
    name = StringField('Group Title', validators=[InputRequired('Please enter a group title')])
    desc = TextAreaField('Description')
    users = SelectMultipleField('Users', validators=[], choices=[], widget=select2MultipleWidget())
