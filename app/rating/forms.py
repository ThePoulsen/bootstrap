## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired
from app.services.services import select2MultipleWidget, select2Widget

class ratingForm(FlaskForm):
    value = IntegerField('Severity value',[InputRequired('Please enter a Severity value')])
    desc = TextAreaField('Description')
    probability = SelectField('Probability', choices=[], validators=[InputRequired('Please select a Probability')], widget=select2Widget())
    impact = SelectField('Impact', choices=[], validators=[InputRequired('Please select a Impact')], widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
