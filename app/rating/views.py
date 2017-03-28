from flask import render_template, Blueprint, request, session, redirect, url_for
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, getUser
import crud
from app.crud import impactCrud, probabilityCrud
from forms import ratingForm

ratingBP = Blueprint('ratingBP', __name__)

@ratingBP.route('/rating', methods=['GET','POST'])
@ratingBP.route('/rating/<string:function>', methods=['GET','POST'])
@ratingBP.route('/rating/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def ratingView(function=None, uuid=None):
    # Universal vars
    viewName = 'Rating'
    viewURL = 'ratingBP.ratingView'
    listColumns = ['Rating', 'Description', 'Probability', 'Impact']
    templateView = 'rating/rating.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'maxDataTableWidth': '700',
              'minDataTableWidth': '500',
              'details': False}

    # Cruds
    listCrud = crud.ratingListData
    getCrud = crud.getRating
    postCrud = crud.postRating
    putCrud = crud.putRating
    deleteCrud = crud.deleteRating

    postForm = ratingForm()
    postData = {'value':postForm.value.data,
                'desc':postForm.desc.data,
                'probability':postForm.probability.data,
                'impact':postForm.impact.data}

    putForm = ratingForm()
    putData = {'value':putForm.value.data,
               'desc':putForm.desc.data,
               'probability':putForm.probability.data,
               'impact':putForm.impact.data}

    # put variables
    putExecs = ['data = getCrud(uuid)',
                'impact=data.impact.uuid if data.impact else ""',
                'probability=data.probability.uuid if data.probability else ""',
                'putForm = ratingForm(value=data.value,desc=data.desc,impact=impact,probability=probability)',
                'impacts = impactCrud.impactSelectData()',
                'impacts.insert(0,("","Select Impact"))',
                'probabilies = probabilityCrud.probabilitySelectData()',
                'probabilies.insert(0,("","Probability"))',
                'putForm.probability.choices = probabilies',
                'putForm.impact.choices = impacts']

    # Post variables
    postExecs = ['impacts = impactCrud.impactSelectData()',
                 'impacts.insert(0,("","Select Impact"))',
                 'probabilies = probabilityCrud.probabilitySelectData()',
                 'probabilies.insert(0,("","Select Probability"))',
                 'postForm.probability.choices = probabilies',
                 'postForm.impact.choices = impacts']

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

@ratingBP.route('/ratingMatrix', methods=['GET'])
def ratingMatrixView():
    kwargs = {}
    impacts = [{'value':i.value,
                'impact':i.title,
                'cost':i.cost,
                'schedule':i.schedule,
                'requirements':i.requirements,
                'legal':i.legal,
                'other':i.other,} for i in impactCrud.getImpacts()]
    probabilities = [{'value':i.value,'probability':i.title} for i in probabilityCrud.getProbabilities()]
    data = [{'impact':r.impact.value,'probability':r.probability.value,'rating':r.value,'desc':r.desc} for r in crud.getRatings()]


    impacts = sorted(impacts, key=lambda k: k['value'], reverse=True)
    probabilities = sorted(probabilities, key=lambda k: k['value'])

    kwargs['impacts'] = impacts
    kwargs['probabilities'] = probabilities
    kwargs['data'] = data

    return render_template('rating/ratingMatrix.html', **kwargs)
