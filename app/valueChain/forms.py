## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired
from app.services.services import select2MultipleWidget, select2Widget

class valueChainForm(FlaskForm):
    title = StringField('Value Chain',[InputRequired('Please enter a Value Chain Title')])
    desc = TextAreaField('Description')
    valueChainArea = SelectField('Value Chain Area', choices=[], validators=[InputRequired('Please select a Value Chain Area')], widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
