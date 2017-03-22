## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for, jsonify
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, getUser
import crud
from app.crud import treatmentTypeCrud, riskResponseCrud
from forms import treatmentForm

treatmentBP = Blueprint('treatmentBP', __name__)

@treatmentBP.route('/treatment', methods=['GET','POST'])
@treatmentBP.route('/treatment/<string:function>', methods=['GET','POST'])
@treatmentBP.route('/treatment/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def treatmentView(function=None, uuid=None):
    # Universal vars
    viewName = 'Treatment'
    viewURL = 'treatmentBP.treatmentView'
    listColumns = ['Treatment', 'Description', 'Treatment Type', 'Risk Response']
    templateView = 'treatment/treatment.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = crud.treatmentListData
    getCrud = crud.getTreatment
    postCrud = crud.postTreatment
    putCrud = crud.putTreatment
    deleteCrud = crud.deleteTreatment

    postForm = treatmentForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data,
                'treatmentType':postForm.treatmentType.data,
                'riskResponse':postForm.riskResponse.data}

    putForm = treatmentForm()
    putData = {'title':putForm.title.data,
               'desc':putForm.desc.data,
               'treatmentType':putForm.treatmentType.data,
               'riskResponse':putForm.riskResponse.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'treatmentType=data.treatmentType.uuid if data.treatmentType else ""',
                'riskResponse=data.riskResponse.uuid if data.riskResponse else ""',
                'putForm = treatmentForm(title=data.title, desc=data.desc, treatmentType=treatmentType, riskResponse=riskResponse)',
                'treatmentTypes =  treatmentTypeCrud.treatmentTypeSelectData()',
                'treatmentTypes.insert(0,("","Select treatmentType"))',
                'putForm.treatmentType.choices = treatmentTypes',
                'riskResponses = riskResponseCrud.riskResponseSelectData()',
                'riskResponses.insert(0,("","Select Risk Response"))',
                'putForm.riskResponse.choices = riskResponses']

    # Post variables
    postExecs = ['treatmentTypes = treatmentTypeCrud.treatmentTypeSelectData()',
                 'treatmentTypes.insert(0,("","Select Treatment Type"))',
                 'postForm.treatmentType.choices = treatmentTypes',
                 'riskResponses = riskResponseCrud.riskResponseSelectData()',
                 'riskResponses.insert(0,("","Select Risk Response"))',
                 'postForm.riskResponse.choices = riskResponses']

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
