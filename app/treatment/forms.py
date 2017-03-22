## -*- coding: utf-8 -*-## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired
from app.services.services import select2Widget

class treatmentForm(FlaskForm):
    title = StringField('Treatment',[InputRequired('Please enter a treatment Title')])
    desc = TextAreaField('Description')
    treatmentType = SelectField('Treatment Type', choices=[], validators=[InputRequired('Please select a Treatment Type')], widget=select2Widget())
    riskResponse = SelectField('Risk Response', choices=[], validators=[InputRequired('Please select a Risk Response')], widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
