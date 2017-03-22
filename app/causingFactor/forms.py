## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired
from app.services.services import select2MultipleWidget, select2Widget

class causingFactorForm(FlaskForm):
    title = StringField('Causing Factor',[InputRequired('Please enter a Causing Factor')])
    desc = TextAreaField('Description')
    causingFactorType = SelectField('Causing Factor Type', choices=[], validators=[InputRequired('Please enter a Causing Factor Type')], widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
