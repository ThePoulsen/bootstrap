## -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField, TextAreaField, IntegerField
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
    region = SelectField('Region', widget=select2Widget(), validators=[InputRequired('Please select a Region')])
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class countryForm(FlaskForm):
    title = StringField('Country title',[InputRequired('Please enter a Country title')])
    abbr = StringField('Country Abbreviation', [InputRequired("Please enter an abbreviation for the Country title")])
    subRegion = SelectField('Sub Region', widget=select2Widget(), validators=[InputRequired('Please select a Sub Region')])
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class zoneForm(FlaskForm):
    title = StringField('Zone title',[InputRequired('Please enter a Zone title')])
    abbr = StringField('Zone Abbreviation', [InputRequired("Please enter an abbreviation for the Zone title")])
    country = SelectField('Country', widget=select2Widget(), validators=[InputRequired('Please select a Country')])
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class statusForm(FlaskForm):
    title = StringField('Status title',[InputRequired('Please enter a Status title')])
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class treatmentTypeForm(FlaskForm):
    title = StringField('Treatment Type',[InputRequired('Please enter a Treatment Type')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class riskResponseForm(FlaskForm):
    title = StringField('Risk Response',[InputRequired('Please enter a Risk Response')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class eventTypeForm(FlaskForm):
    title = StringField('Event Type',[InputRequired('Please enter a Event Type')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class impactForm(FlaskForm):
    value = IntegerField('Value',[InputRequired('Please enter a Impact Value')])
    title = StringField('Impact',[InputRequired('Please enter a Impact')])
    cost = TextAreaField('Cost')
    schedule = TextAreaField('Schedule')
    requirements = TextAreaField('Requirements')
    legal = TextAreaField('Legal')
    other = TextAreaField('Other')
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class probabilityForm(FlaskForm):
    value = IntegerField('Value',[InputRequired('Please enter a Probability Value')])
    title = StringField('Probability',[InputRequired('Please enter a Probability')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class causingFactorTypeForm(FlaskForm):
    title = StringField('Causing Factor Type',[InputRequired('Please select a Causing Factor Type')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class processAreaForm(FlaskForm):
    title = StringField('Process Area',[InputRequired('Please enter a Process Area')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class riskAreaForm(FlaskForm):
    title = StringField('Risk Area',[InputRequired('Please enter a Risk Area')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class riskTypeForm(FlaskForm):
    title = StringField('Risk Type',[InputRequired('Please enter a Risk Type')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class valueChainAreaForm(FlaskForm):
    title = StringField('Value Chain Area',[InputRequired('Please enter a Value Chain Area')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class valueChainStepTypeForm(FlaskForm):
    title = StringField('Value Chain Step Type',[InputRequired('Please enter a Value Chain Step Type')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')

class deliveryPointForm(FlaskForm):
    title = StringField('Delivery Point',[InputRequired('Please enter a Delivery Point')])
    desc = TextAreaField('Description')
    submit = SubmitField(label='Save')
    submitStay = SubmitField(label='Save and add new')
