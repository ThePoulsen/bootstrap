from flask import render_template, Blueprint, request, session, redirect, url_for
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, getUser
import crud
from app.crud import causingFactorTypeCrud
from forms import causingFactorForm

causingFactorBP = Blueprint('causingFactorBP', __name__)

@causingFactorBP.route('/causingFactor', methods=['GET','POST'])
@causingFactorBP.route('/causingFactor/<string:function>', methods=['GET','POST'])
@causingFactorBP.route('/causingFactor/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def causingFactorView(function=None, uuid=None):
    # Universal vars
    viewName = 'Causing Factor'
    viewURL = 'causingFactorBP.causingFactorView'
    listColumns = ['Causing Factor', 'Description', 'Causing Factor Type']
    templateView = 'causingFactor/causingFactor.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = crud.causingFactorListData
    getCrud = crud.getCausingFactor
    postCrud = crud.postCausingFactor
    putCrud = crud.putCausingFactor
    deleteCrud = crud.deleteCausingFactor

    postForm = causingFactorForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data,
                'causingFactorType':postForm.causingFactorType.data}

    putForm = causingFactorForm()
    putData = {'title':putForm.title.data,
               'desc':putForm.desc.data,
               'causingFactorType':putForm.causingFactorType.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'causingFactorType=data.causingFactorType.uuid if data.causingFactorType else ""',
                'putForm = causingFactorForm(title=data.title,desc=data.desc,causingFactorType=causingFactorType)',
                'causingFactors =  causingFactorTypeCrud.causingFactorTypeSelectData()',
                'causingFactors.insert(0,("","Select Causing Factor Type"))',
                'putForm.causingFactorType.choices = causingFactors']

    # Post variables
    postExecs = ['causingFactors = causingFactorTypeCrud.causingFactorTypeSelectData()',
                 'causingFactors.insert(0,("","Select Causing Factor Type"))',
                 'postForm.causingFactorType.choices = causingFactors',]

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
