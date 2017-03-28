## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, session, redirect, url_for
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, getUser
from app.crud import regionCrud, subRegionCrud, countryCrud, zoneCrud, statusCrud, treatmentTypeCrud, riskResponseCrud, eventTypeCrud, impactCrud, probabilityCrud, causingFactorTypeCrud, processAreaCrud, riskAreaCrud, riskTypeCrud, valueChainAreaCrud, deliveryPointCrud, valueChainStepTypeCrud
from forms import regionForm, subRegionForm, countryForm, zoneForm, statusForm, treatmentTypeForm, riskResponseForm, eventTypeForm, impactForm, probabilityForm, causingFactorTypeForm, processAreaForm, riskAreaForm, riskTypeForm, valueChainAreaForm, deliveryPointForm, valueChainStepTypeForm

mdBP = Blueprint('mdBP', __name__)

@mdBP.route('/region', methods=['GET','POST'])
@mdBP.route('/region/<string:function>', methods=['GET','POST'])
@mdBP.route('/region/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def regionView(function=None, uuid=None):
    # Universal vars
    viewName = 'Region'
    viewURL = 'mdBP.regionView'
    listColumns = ['Region', 'Region abbreviation', 'Sub Regions']
    templateView = 'masterData/region.html'
    
    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}
    
    # Cruds
    listCrud = regionCrud.regionListData
    getCrud = regionCrud.getRegion
    postCrud = regionCrud.postRegion
    putCrud = regionCrud.putRegion
    deleteCrud = regionCrud.deleteRegion

    postForm = regionForm()
    postData = {'title':postForm.title.data,
                'abbr':postForm.abbr.data,
                'subRegions':postForm.subRegions.data}

    putForm = regionForm()
    putData = {'title':putForm.title.data,
               'abbr':putForm.abbr.data,
               'subRegions':putForm.subRegions.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'subReg = [r.uuid for r in data.subRegions]',
                'putForm = regionForm(title=data.title,abbr=data.abbr,subRegions=subReg)',
                'subRegions = subRegionCrud.subRegionSelectData()',
                'putForm.subRegions.choices = subRegions']

    # Post variables
    postExecs = ['subRegions = subRegionCrud.subRegionSelectData()',
                 'postForm.subRegions.choices = subRegions']

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)
    
    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}
        
        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)
    
    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}
        
        return render_template(templateView, **kwargs)
    
    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}
        
        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)
    
    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/subRegion', methods=['GET','POST'])
@mdBP.route('/subRegion/<string:function>', methods=['GET','POST'])
@mdBP.route('/subRegion/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def subRegionView(function=None, uuid=None):
    # Universal vars
    viewName = 'Sub Region'
    viewURL = 'mdBP.subRegionView'
    listColumns = ['Sub Region', 'Sub Region abbreviation', 'Region']
    templateView = 'masterData/subRegion.html'
    
    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = subRegionCrud.subRegionListData
    getCrud = subRegionCrud.getSubRegion
    postCrud = subRegionCrud.postSubRegion
    putCrud = subRegionCrud.putSubRegion
    deleteCrud = subRegionCrud.deleteSubRegion
    
    postForm = subRegionForm()
    postData = {'title':postForm.title.data,
                'abbr':postForm.abbr.data,
                'region':postForm.region.data}

    putForm = subRegionForm()
    putData = {'title':putForm.title.data,
               'abbr':putForm.abbr.data,
               'region':putForm.region.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = subRegionForm(title=data.title,abbr=data.abbr,region=data.region.uuid if data.region else "")',
                'regions = regionCrud.regionSelectData()',
                'regions.insert(0,("","Select Region"))',
                'putForm.region.choices = regions']

    # Post variables
    postExecs = ['regions = regionCrud.regionSelectData()',
                 'regions.insert(0,("","Select Region"))',
                 'postForm.region.choices = regions',]

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)
    
    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}
        
        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)
    
    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}
        
        return render_template(templateView, **kwargs)
    
    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}
        
        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)
    
    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/country', methods=['GET','POST'])
@mdBP.route('/country/<string:function>', methods=['GET','POST'])
@mdBP.route('/country/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def countryView(function=None, uuid=None):
    # Universal vars
    viewName = 'Country'
    viewURL = 'mdBP.countryView'
    listColumns = ['Country', 'Country abbreviation', 'Sub Region']
    templateView = 'masterData/country.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = countryCrud.countryListData
    getCrud = countryCrud.getCountry
    postCrud = countryCrud.postCountry
    putCrud = countryCrud.putCountry
    deleteCrud = countryCrud.deleteCountry

    postForm = countryForm()
    postData = {'title':postForm.title.data,
                'abbr':postForm.abbr.data,
                'subRegion':postForm.subRegion.data}

    putForm = countryForm()
    putData = {'title':putForm.title.data,
               'abbr':putForm.abbr.data,
               'subRegion':putForm.subRegion.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = countryForm(title=data.title,abbr=data.abbr,subRegion=data.subRegion.uuid if data.subRegion else "")',
                'subRegions = subRegionCrud.subRegionSelectData()',
                'subRegions.insert(0,("","Select Sub Region"))',
                'putForm.subRegion.choices = subRegions']

    # Post variables
    postExecs = ['subRegions = subRegionCrud.subRegionSelectData()',
                 'subRegions.insert(0,("","Select Sub Region"))',
                 'postForm.subRegion.choices = subRegions']

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/zone', methods=['GET','POST'])
@mdBP.route('/zone/<string:function>', methods=['GET','POST'])
@mdBP.route('/zone/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def zoneView(function=None, uuid=None):
    # Universal vars
    viewName = 'Zone'
    viewURL = 'mdBP.zoneView'
    listColumns = ['Zone', 'Zone abbreviation', 'Country']
    templateView = 'masterData/zone.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = zoneCrud.zoneListData
    getCrud = zoneCrud.getZone
    postCrud = zoneCrud.postZone
    putCrud = zoneCrud.putZone
    deleteCrud = zoneCrud.deleteZone

    postForm = zoneForm()
    postData = {'title':postForm.title.data,
                'abbr':postForm.abbr.data,
                'country':postForm.country.data}

    putForm = zoneForm()
    putData = {'title':putForm.title.data,
               'abbr':putForm.abbr.data,
               'country':putForm.country.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = zoneForm(title=data.title,abbr=data.abbr,country=data.country.uuid if data.country else "")',
                'countries = countryCrud.countrySelectData()',
                'countries.insert(0,("","Select Country"))',
                'putForm.country.choices = countries']

    # Post variables
    postExecs = ['countries = countryCrud.countrySelectData()',
                 'countries.insert(0,("","Select Country"))',
                 'postForm.country.choices = countries']

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/status', methods=['GET','POST'])
@mdBP.route('/status/<string:function>', methods=['GET','POST'])
@mdBP.route('/status/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def statusView(function=None, uuid=None):
    # Universal vars
    viewName = 'Status'
    viewURL = 'mdBP.statusView'
    listColumns = ['Status']
    templateView = 'masterData/status.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = statusCrud.statusListData
    getCrud = statusCrud.getStatus
    postCrud = statusCrud.postStatus
    putCrud = statusCrud.putStatus
    deleteCrud = statusCrud.deleteStatus

    postForm = statusForm()
    postData = {'title':postForm.title.data}

    putForm = statusForm()
    putData = {'title':putForm.title.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = statusForm(title=data.title)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/treatmentType', methods=['GET','POST'])
@mdBP.route('/treatmentType/<string:function>', methods=['GET','POST'])
@mdBP.route('/treatmentType/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def treatmentTypeView(function=None, uuid=None):
    # Universal vars
    viewName = 'Treatment Type'
    viewURL = 'mdBP.treatmentTypeView'
    listColumns = ['Treatment Type','Description']
    templateView = 'masterData/treatmentType.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = treatmentTypeCrud.treatmentTypeListData
    getCrud = treatmentTypeCrud.getTreatmentType
    postCrud = treatmentTypeCrud.postTreatmentType
    putCrud = treatmentTypeCrud.putTreatmentType
    deleteCrud = treatmentTypeCrud.deleteTreatmentType

    postForm = treatmentTypeForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = treatmentTypeForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = treatmentTypeForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/riskResponse', methods=['GET','POST'])
@mdBP.route('/riskResponse/<string:function>', methods=['GET','POST'])
@mdBP.route('/riskResponse/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def riskResponseView(function=None, uuid=None):
    # Universal vars
    viewName = 'Risk Response'
    viewURL = 'mdBP.riskResponseView'
    listColumns = ['Risk Response','Description']
    templateView = 'masterData/riskResponse.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = riskResponseCrud.riskResponseListData
    getCrud = riskResponseCrud.getRiskResponse
    postCrud = riskResponseCrud.postRiskResponse
    putCrud = riskResponseCrud.putRiskResponse
    deleteCrud = riskResponseCrud.deleteRiskResponse

    postForm = riskResponseForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = riskResponseForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = riskResponseForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/eventType', methods=['GET','POST'])
@mdBP.route('/eventType/<string:function>', methods=['GET','POST'])
@mdBP.route('/eventType/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def eventTypeView(function=None, uuid=None):
    # Universal vars
    viewName = 'Event Type'
    viewURL = 'mdBP.eventTypeView'
    listColumns = ['Event Type','Description']
    templateView = 'masterData/eventType.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = eventTypeCrud.eventTypeListData
    getCrud = eventTypeCrud.getEventType
    postCrud = eventTypeCrud.postEventType
    putCrud = eventTypeCrud.putEventType
    deleteCrud = eventTypeCrud.deleteEventType

    postForm = eventTypeForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = eventTypeForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = eventTypeForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/impact', methods=['GET','POST'])
@mdBP.route('/impact/<string:function>', methods=['GET','POST'])
@mdBP.route('/impact/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def impactView(function=None, uuid=None):
    # Universal vars
    viewName = 'Impact'
    viewURL = 'mdBP.impactView'
    listColumns = ['Value', 'Impact', 'Cost', 'Schedule', 'Requirements', 'Legal', 'Other']
    templateView = 'masterData/impact.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'details': False}

    # Cruds
    listCrud = impactCrud.impactListData
    getCrud = impactCrud.getImpact
    postCrud = impactCrud.postImpact
    putCrud = impactCrud.putImpact
    deleteCrud = impactCrud.deleteImpact

    postForm = impactForm()
    postData = {'title':postForm.title.data,
                'cost':postForm.cost.data,
                'schedule':postForm.schedule.data,
                'requirements':postForm.requirements.data,
                'legal':postForm.legal.data,
                'other':postForm.other.data,
                'value':postForm.value.data}

    putForm = impactForm()
    putData = {'title':putForm.title.data,
               'cost':putForm.cost.data,
               'schedule':putForm.schedule.data,
               'requirements':putForm.requirements.data,
               'legal':putForm.legal.data,
               'other':putForm.other.data,
               'value':putForm.value.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'dataKwargs = {"title":data.title}',
                'dataKwargs["cost"] = data.cost',
                'dataKwargs["schedule"] = data.schedule',
                'dataKwargs["requirements"] = data.requirements',
                'dataKwargs["legal"] = data.legal',
                'dataKwargs["other"] = data.other',
                'dataKwargs["value"] = data.value',
                'putForm = impactForm(**dataKwargs)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/probability', methods=['GET','POST'])
@mdBP.route('/probability/<string:function>', methods=['GET','POST'])
@mdBP.route('/probability/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def probabilityView(function=None, uuid=None):
    # Universal vars
    viewName = 'Probability'
    viewURL = 'mdBP.probabilityView'
    listColumns = ['Value', 'Probability','Description']
    templateView = 'masterData/probability.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = probabilityCrud.probabilityListData
    getCrud = probabilityCrud.getProbability
    postCrud = probabilityCrud.postProbability
    putCrud = probabilityCrud.putProbability
    deleteCrud = probabilityCrud.deleteProbability

    postForm = probabilityForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data,
                'value':postForm.value.data}

    putForm = probabilityForm()
    putData = {'title':putForm.title.data,
               'desc':putForm.desc.data,
               'value':putForm.value.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = probabilityForm(title=data.title, desc=data.desc, value=data.value)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/causingFactorType', methods=['GET','POST'])
@mdBP.route('/causingFactorType/<string:function>', methods=['GET','POST'])
@mdBP.route('/causingFactorType/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def causingFactorTypeView(function=None, uuid=None):
    # Universal vars
    viewName = 'Causing Factor Type'
    viewURL = 'mdBP.causingFactorTypeView'
    listColumns = ['Causing Factor Type','Description']
    templateView = 'masterData/causingFactorType.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = causingFactorTypeCrud.causingFactorTypeListData
    getCrud = causingFactorTypeCrud.getCausingFactorType
    postCrud = causingFactorTypeCrud.postCausingFactorType
    putCrud = causingFactorTypeCrud.putCausingFactorType
    deleteCrud = causingFactorTypeCrud.deleteCausingFactorType

    postForm = causingFactorTypeForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = causingFactorTypeForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = causingFactorTypeForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/processArea', methods=['GET','POST'])
@mdBP.route('/processArea/<string:function>', methods=['GET','POST'])
@mdBP.route('/processArea/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def processAreaView(function=None, uuid=None):
    # Universal vars
    viewName = 'Process Area'
    viewURL = 'mdBP.processAreaView'
    listColumns = ['Process Area','Description']
    templateView = 'masterData/processArea.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = processAreaCrud.processAreaListData
    getCrud = processAreaCrud.getProcessArea
    postCrud = processAreaCrud.postProcessArea
    putCrud = processAreaCrud.putProcessArea
    deleteCrud = processAreaCrud.deleteProcessArea

    postForm = processAreaForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = processAreaForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = processAreaForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/riskArea', methods=['GET','POST'])
@mdBP.route('/riskArea/<string:function>', methods=['GET','POST'])
@mdBP.route('/riskArea/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def riskAreaView(function=None, uuid=None):
    # Universal vars
    viewName = 'Risk Area'
    viewURL = 'mdBP.riskAreaView'
    listColumns = ['Risk Area','Description']
    templateView = 'masterData/riskArea.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = riskAreaCrud.riskAreaListData
    getCrud = riskAreaCrud.getRiskArea
    postCrud = riskAreaCrud.postRiskArea
    putCrud = riskAreaCrud.putRiskArea
    deleteCrud = riskAreaCrud.deleteRiskArea

    postForm = riskAreaForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = riskAreaForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = riskAreaForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/riskType', methods=['GET','POST'])
@mdBP.route('/riskType/<string:function>', methods=['GET','POST'])
@mdBP.route('/riskType/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def riskTypeView(function=None, uuid=None):
    # Universal vars
    viewName = 'Risk Type'
    viewURL = 'mdBP.riskTypeView'
    listColumns = ['Risk Type','Description']
    templateView = 'masterData/riskType.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = riskTypeCrud.riskTypeListData
    getCrud = riskTypeCrud.getRiskType
    postCrud = riskTypeCrud.postRiskType
    putCrud = riskTypeCrud.putRiskType
    deleteCrud = riskTypeCrud.deleteRiskType

    postForm = riskTypeForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = riskTypeForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = riskTypeForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/valueChainArea', methods=['GET','POST'])
@mdBP.route('/valueChainArea/<string:function>', methods=['GET','POST'])
@mdBP.route('/valueChainArea/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def valueChainAreaView(function=None, uuid=None):
    # Universal vars
    viewName = 'Value Chain Area'
    viewURL = 'mdBP.valueChainAreaView'
    listColumns = ['Value Chain Area','Description']
    templateView = 'masterData/valueChainArea.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = valueChainAreaCrud.valueChainAreaListData
    getCrud = valueChainAreaCrud.getValueChainArea
    postCrud = valueChainAreaCrud.postValueChainArea
    putCrud = valueChainAreaCrud.putValueChainArea
    deleteCrud = valueChainAreaCrud.deleteValueChainArea

    postForm = valueChainAreaForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = valueChainAreaForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = valueChainAreaForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/valueChainStepType', methods=['GET','POST'])
@mdBP.route('/valueChainStepType/<string:function>', methods=['GET','POST'])
@mdBP.route('/valueChainStepType/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def valueChainStepTypeView(function=None, uuid=None):
    # Universal vars
    viewName = 'Value Chain Step Type'
    viewURL = 'mdBP.valueChainStepTypeView'
    listColumns = ['Value Chain Step Type','Description']
    templateView = 'masterData/valueChainStepType.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = valueChainStepTypeCrud.valueChainStepTypeListData
    getCrud = valueChainStepTypeCrud.getValueChainStepType
    postCrud = valueChainStepTypeCrud.postValueChainStepType
    putCrud = valueChainAreaCrud.putValueChainArea
    deleteCrud = valueChainStepTypeCrud.deleteValueChainStepType

    postForm = valueChainStepTypeForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = valueChainStepTypeForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm = valueChainStepTypeForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))

@mdBP.route('/deliveryPoint', methods=['GET','POST'])
@mdBP.route('/deliveryPoint/<string:function>', methods=['GET','POST'])
@mdBP.route('/deliveryPoint/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def deliveryPointView(function=None, uuid=None):
    # Universal vars
    viewName = 'Delivery Point'
    viewURL = 'mdBP.deliveryPointView'
    listColumns = ['Delivery Point','Description']
    templateView = 'masterData/deliveryPoint.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = deliveryPointCrud.deliveryPointListData
    getCrud = deliveryPointCrud.getDeliveryPoint
    postCrud = deliveryPointCrud.postDeliveryPoint
    putCrud = deliveryPointCrud.putDeliveryPoint
    deleteCrud = deliveryPointCrud.deleteDeliveryPoint

    postForm = deliveryPointForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data}

    putForm = deliveryPointForm()
    putData = {'title':putForm.title.data,
                'desc':putForm.desc.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'putForm =deliveryPointForm(title=data.title, desc=data.desc)']

    # Post variables
    postExecs = []

    # --------------------------------------------------------------------------------------------
    # CRUD Views (Do not touch!)
    # Build list of all rows
    if function == None:
        kwargs['listColumns'] = listColumns
        kwargs['listData'] = listCrud()
        return render_template('dataTable.html', **kwargs)

    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName),
                  'submitStay': True}

        for r in postExecs:
            exec(r)

        if postForm.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                if not postForm.submitStay.data:
                    return redirect(url_for(viewURL))
                else:
                    return redirect(url_for(viewURL)+'/new')
            elif 'error' in req:
                errorMessage(req['error'])
        return render_template(templateView, form=postForm, **kwargs)

    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        data = getCrud(uuid)
        kwargs = {'contentTitle': '{} details'.format(viewName),
                  'details': True,
                  'detailsData':data,
                  'submitStay': False,
                  'modifiedUser':getUser(data.modifiedBy),
                  'createdUser':getUser(data.createdBy)}

        return render_template(templateView, **kwargs)

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

        if putForm.validate_on_submit():
            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))
