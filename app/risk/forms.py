## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField, IntegerField, StringField
from wtforms.validators import InputRequired
from app.services.services import select2MultipleWidget, select2Widget

class riskForm(FlaskForm):
    title = StringField('Risk Title',[InputRequired('Please enter a Risk title')])
    desc = TextAreaField('Description')
    probability = SelectField('Probability', choices=[], validators=[InputRequired('Please select a Probability')], widget=select2Widget())
    impact = SelectField('Impact', choices=[], validators=[InputRequired('Please select an Impact')], widget=select2Widget())
    riskArea = SelectField('Risk Area', choices=[], validators=[InputRequired('Please select a Risk Area')], widget=select2Widget())
    riskType = SelectField('Risk Type', choices=[], validators=[InputRequired('Please select a Risk Type')], widget=select2Widget())
    owner = SelectField('Owner', choices=[], validators=[InputRequired('Please select an Owner')], widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
