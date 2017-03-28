## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, session, redirect, url_for
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, getUser
import crud
from app.crud import riskAreaCrud, riskTypeCrud, impactCrud, probabilityCrud, userCrud
from forms import riskForm

riskBP = Blueprint('riskBP', __name__)

@riskBP.route('/risk', methods=['GET','POST'])
@riskBP.route('/risk/<string:function>', methods=['GET','POST'])
@riskBP.route('/risk/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def riskView(function=None, uuid=None):
    # Universal vars
    viewName = 'Risk'
    viewURL = 'riskBP.riskView'
    listColumns = ['Risk', 'Description', 'Impact', 'Probability', 'Risk Rating', 'Created', 'Author', 'Owner']
    templateView = 'risk/risk.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'details': False}

    # Cruds
    listCrud = crud.riskListData
    getCrud = crud.getRisk
    postCrud = crud.postRisk
    putCrud = crud.putRisk
    deleteCrud = crud.deleteRisk

    postForm = riskForm()
    postData = {'title':postForm.title.data,
                'desc':postForm.desc.data,
                'probability':postForm.probability.data,
                'impact':postForm.impact.data,
                'riskArea':postForm.riskArea.data,
                'riskType':postForm.riskType.data,
                'owner':postForm.owner.data}

    putForm = riskForm()
    putData = {'title':putForm.title.data,
               'desc':putForm.desc.data,
               'probability':putForm.probability.data,
               'impact':putForm.impact.data,
               'riskArea':putForm.riskArea.data,
               'riskType':putForm.riskType.data,
               'owner':putForm.owner.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'impact=data.impact.uuid if data.impact else ""',
                'probability=data.probability.uuid if data.probability else ""',
                'riskArea=data.riskArea.uuid if data.riskArea else ""',
                'riskType=data.riskType.uuid if data.riskType else ""',
                'putForm = riskForm(title=data.title,desc=data.desc,impact=impact,probability=probability, riskArea=riskArea, riskType=riskType, owner=data.owner)',
                'impacts = impactCrud.impactSelectData()',
                'impacts.insert(0,("","Select Impact"))',
                'probabilies = probabilityCrud.probabilitySelectData()',
                'probabilies.insert(0,("","Probability"))',
                'riskAreas = riskAreaCrud.riskAreaSelectData()',
                'riskAreas.insert(0,("","Select Risk Area"))',
                'riskTypes = riskTypeCrud.riskTypeSelectData()',
                'riskTypes.insert(0,("","Select Risk Type"))',
                'owners = userCrud.userSelectData()',
                'owners.insert(0,("","Select User"))',
                'putForm.probability.choices = probabilies',
                'putForm.impact.choices = impacts',
                'putForm.riskArea.choices = riskAreas',
                'putForm.riskType.choices = riskTypes',
                'putForm.owner.choices = owners']

    # Post variables
    postExecs = ['impacts = impactCrud.impactSelectData()',
                 'impacts.insert(0,("","Select Impact"))',
                 'probabilies = probabilityCrud.probabilitySelectData()',
                 'probabilies.insert(0,("","Select Probability"))',
                 'riskAreas = riskAreaCrud.riskAreaSelectData()',
                 'riskAreas.insert(0,("","Select Risk Area"))',
                 'riskTypes = riskTypeCrud.riskTypeSelectData()',
                 'riskTypes.insert(0,("","Select Risk Type"))',
                 'owners = userCrud.userSelectData()',
                 'owners.insert(0,("","Select User"))',
                 'postForm.probability.choices = probabilies',
                 'postForm.impact.choices = impacts',
                 'postForm.riskArea.choices = riskAreas',
                 'postForm.riskType.choices = riskTypes',
                 'postForm.owner.choices = owners']

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
