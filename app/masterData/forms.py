## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import InputRequired
from app.services.services import select2MultipleWidget, select2Widget

class regionForm(FlaskForm):
    title = StringField('Region title',[InputRequired('Please enter a Region title')])
    abbr = StringField('Region Abbreviation', [InputRequired("Please enter an abbreviation for the Region title")])
    subRegions = SelectMultipleField('Sub Regions', widget=select2MultipleWidget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class subRegionForm(FlaskForm):
    title = StringField('Sub Region title',[InputRequired('Please enter a Sub Region title')])
    abbr = StringField('Sub Region Abbreviation', [InputRequired("Please enter an abbreviation for the Sub Region title")])
    region = SelectField('Region', widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class countryForm(FlaskForm):
    title = StringField('Country title',[InputRequired('Please enter a Country title')])
    abbr = StringField('Country Abbreviation', [InputRequired("Please enter an abbreviation for the Country title")])
    subRegion = SelectField('Sub Region', widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class zoneForm(FlaskForm):
    title = StringField('Zone title',[InputRequired('Please enter a Zone title')])
    abbr = StringField('Zone Abbreviation', [InputRequired("Please enter an abbreviation for the Zone title")])
    country = SelectField('Country', widget=select2Widget())
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class statusForm(FlaskForm):
    title = StringField('Status title',[InputRequired('Please enter a Status title')])
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
