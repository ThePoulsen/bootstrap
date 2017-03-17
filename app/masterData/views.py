## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, session, redirect, url_for
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole
from app.crud import regionCrud, subRegionCrud
from forms import regionForm

mdBP = Blueprint('mdBP', __name__)

# profileView
@mdBP.route('/region', methods=['GET','POST'])
@mdBP.route('/region/<string:function>', methods=['GET','POST'])
@mdBP.route('/region/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def regionView(function=None, uuid=None):
    # Universal vars
    viewName = 'Region list'
    viewURL = 'mdBP.regionView'
    tableColumns = ['Region', 'Region abbreviation', 'Sub Regions']
    tableData = regionCrud.getRegions()
    templateView = 'masterData/region.html'
    form = regionForm()
    postCrud = regionCrud.postRegion
    postData = {'title':form.title.data,
                'abbr':form.abbr.data}
    deleteCrud = regionCrud.deleteRegion
    
    # View kwargs
    kwargs = {'title': viewName,
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500'}
    
    # Build list of all rows
    if function == None:
        kwargs['tableColumns'] = tableColumns
        kwargs['tableData'] = tableData
        
        return render_template('dataTable.html', **kwargs)
    
    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName)}
        
        if form.validate_on_submit():
            req = postCrud(data = postData)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=form, **kwargs)

    
    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': '{} details'.format(viewName)}
        
        pass
    
    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}.format(viewName)'}
        
        pass
    
    # Delete single row
    elif function == 'delete' and uuid != None:
        req = deleteCrud(uuid)
        if 'success' in req:
            successMessage(req['success'])
        elif 'error' in req:
            errorMessage(req['error'])
        return redirect(url_for(viewURL))
            
    

# profileView
@mdBP.route('/subRegion', methods=['GET','POST'])
@mdBP.route('/subregion/<string:function>', methods=['GET','POST'])
@mdBP.route('/subregion/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator'])
def subRegionView(function=None, uuid=None):
    # Universal vars
    viewName = 'Sub Region list'
    tableColumns = ['Sub Region', 'Sub Region abbreviation', 'Region']
    tableData = subRegionCrud.getSubRegions()
    
    
    # View kwargs
    kwargs = {'title': viewName}    
    
    # Build list of all rows
    if function == None:
        kwargs['tableColumns'] = tableColumns
        kwargs['tableData'] = tableData
        
        return render_template('listView.html', **kwargs)
    
    # Create new row
    elif function == 'new':
        # Function kwargs
        kwargs = {'contentTitle': 'Add new {}'.format(viewName)}
        
        pass
    
    # View single row details
    elif function == 'details' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': '{} details'.format(viewName)}
        
        pass
    
    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}.format(viewName)'}
        
        pass
    
    # Delete single row
    elif function == 'delete' and uuid != None:
        pass
