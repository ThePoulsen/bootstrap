## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, session, redirect, url_for
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, getUser
from app.crud import regionCrud, subRegionCrud, countryCrud, zoneCrud
from forms import regionForm, subRegionForm, countryForm, zoneForm

mdBP = Blueprint('mdBP', __name__)

# Region View
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

# Sub Region View
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
                'regions.insert(0,("0","Select Region"))',
                'putForm.region.choices = regions']

    # Post variables
    postExecs = ['regions = regionCrud.regionSelectData()',
                 'regions.insert(0,("0","Select Region"))',
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

# Country View
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
                'subRegions.insert(0,("0","Select Sub Region"))',
                'putForm.subRegion.choices = subRegions']

    # Post variables
    postExecs = ['subRegions = subRegionCrud.subRegionSelectData()',
                 'subRegions.insert(0,("0","Select Sub Region"))',
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
                'countries.insert(0,("0","Select Country"))',
                'putForm.country.choices = countries']

    # Post variables
    postExecs = ['countries = countryCrud.countrySelectData()',
                 'countries.insert(0,("0","Select Country"))',
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
