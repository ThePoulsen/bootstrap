## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class regionForm(FlaskForm):
    title = StringField('Region title',[InputRequired('Please enter a Region title')])
    abbr = StringField('Region Abbreviation', [InputRequired("Please enter an abbreviation for the Region title")])
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
