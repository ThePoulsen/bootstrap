## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for, jsonify
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, getUser
import crud
from app.crud import valueChainAreaCrud
from forms import valueChainForm

valueChainBP = Blueprint('valueChainBP', __name__)

@valueChainBP.route('/valueChain', methods=['GET','POST'])
@valueChainBP.route('/valueChain/<string:function>', methods=['GET','POST'])
@valueChainBP.route('/valueChain/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def valueChainView(function=None, uuid=None):
    # Universal vars
    viewName = 'Value Chain'
    viewURL = 'valueChainBP.valueChainView'
    listColumns = ['Value Chain', 'Description', 'Value Chain Area']
    templateView = 'valueChain/valueChain.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = crud.valueChainListData
    getCrud = crud.getValueChain
    postCrud = crud.postValueChain
    putCrud = crud.putValueChain
    deleteCrud = crud.deleteValueChain

    postForm = valueChainForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data,
                'valueChainArea':postForm.valueChainArea.data}

    putForm = valueChainForm()
    putData = {'title':putForm.title.data,
               'desc':putForm.desc.data,
               'valueChainArea':putForm.valueChainArea.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'valueChainArea=data.valueChainArea.uuid if data.valueChainArea else ""',
                'putForm = valueChainForm(title=data.title,desc=data.desc,valueChainArea=valueChainArea)',
                'valueChainAreas =  valueChainAreaCrud.valueChainAreaSelectData()',
                'valueChainAreas.insert(0,("","Select Value Chain Area"))',
                'putForm.valueChainArea.choices = valueChainAreas']

    # Post variables
    postExecs = ['valueChainAreas = valueChainAreaCrud.valueChainAreaSelectData()',
                 'valueChainAreas.insert(0,("","Select Value Chain Area"))',
                 'postForm.valueChainArea.choices = valueChainAreas',]

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
