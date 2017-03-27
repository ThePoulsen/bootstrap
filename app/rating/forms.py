## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired
from app.services.services import select2MultipleWidget, select2Widget

class ratingForm(FlaskForm):
    value = IntegerField('Risk Rating',[InputRequired('Please enter a Risk Rating value')])
    desc = TextAreaField('Description')
    probability = SelectField('Probability', choices=[], validators=[InputRequired('Please select a Probability')], widget=select2Widget())
    impact = SelectField('Impact', choices=[], validators=[InputRequired('Please select an Impact')], widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
