## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for, jsonify
from authAPI import authAPI
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, sendMail, getUser, getRole
from forms import userForm, groupForm
from app.crud import userCrud, groupCrud
import os

userBP = Blueprint('userBP', __name__)

# profileView
@userBP.route('/profile', methods=['GET','POST'])
@loginRequired
def profileView():
    user = authAPI(endpoint='user/'+session['user_uuid']+'?includeRoles=True&includeGroups=True', method='get', token=session['token'])
    if 'user' in user:
        return render_template('user/profile.html', user=user['user'])
    else:
        errorMessage('Your user profile is not found')
        return redirect(url_for('indexBP.indexView'))

@userBP.route('/user', methods=['GET'])
@userBP.route('/user/<string:function>', methods=['GET','POST'])
@userBP.route('/user/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def userView(function=None, uuid=None):
    # Universal vars
    viewName = 'User'
    viewURL = 'userBP.userView'
    listColumns = ['Initials','User name','Email','Roles','Groups', 'Locked?', 'Contact?', 'Active?', 'Confirmed?']
    templateView = 'user/user.html'

    # View kwargs
    kwargs = {'title': viewName+' list',
              'details': False,
              'activateButton': True,
              'activeIndex':8,
              'lockButton': True,
              'lockIndex': 6}

    # Cruds
    listCrud = userCrud.userListData
    getCrud = userCrud.getUser
    postCrud = userCrud.postUser
    putCrud = userCrud.putUser
    deactivateCrud = userCrud.deactivateUser
    activateCrud = userCrud.activateUser
    deleteCrud = userCrud.deleteUser
    lockCrud = userCrud.lockUser
    unlockCrud = userCrud.unlockUser

    postForm = userForm(role='User', locked='Locked', active='Active')
    postData = {'initials':postForm.initials.data,
                'name':postForm.name.data,
                'email':postForm.email.data,
                'phone':postForm.phone.data,
                'role':postForm.role.data,
                'groups':postForm.groups.data,
                'contact':False}

    putForm = userForm()
    putData = {'initials':putForm.initials.data,
               'name':putForm.name.data,
               'email':putForm.email.data,
               'phone':putForm.phone.data,
               'groups':putForm.groups.data}

    # put variables
    putExecs = ['data = userCrud.getUser(uuid)',
                'role = getRole(data.role)',
                'groups = [r.uuid for r in data.groups]',
                'putForm = userForm(name=data.name,initials=data.initials,email=data.email,phone=data.phone,role=data.role,groups=groups, locked="Locked", active="Active")',
                'groups = groupCrud.groupSelectData()',
                'postForm.groups.choices = groups']

    # Post variables
    postExecs = ['groups = groupCrud.groupSelectData()',
                 'postForm.groups.choices = groups']

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
            req = postCrud(data=postData)
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

    elif function == 'deactivate' and uuid != None:
        data = userCrud.getUser(uuid)
        if data.role == 'Administrator':
            errorMessage('You cannot change the active status of Administrators')
            return redirect(url_for('userBP.userView'))
        # Function kwargs
        req = deactivateCrud(uuid=uuid)
        if 'success' in req:
            successMessage(req['success'])
            return redirect(url_for(viewURL))
        elif 'error' in req:
            errorMessage(req['error'])

    elif function == 'activate' and uuid != None:
        data = userCrud.getUser(uuid)
        if data.role == 'Administrator':
            errorMessage('You cannot change the active status of Administrators')
            return redirect(url_for('userBP.userView'))
        # Function kwargs
        req = activateCrud(uuid=uuid)
        if 'success' in req:
            successMessage(req['success'])
            return redirect(url_for(viewURL))
        elif 'error' in req:
            errorMessage(req['error'])

    elif function == 'lock' and uuid != None:
        data = userCrud.getUser(uuid)
        if data.role == 'Administrator':
            errorMessage('You cannot lock out Administrators')
            return redirect(url_for('userBP.userView'))
        # Function kwargs
        req = lockCrud(uuid=uuid)
        if 'success' in req:
            successMessage(req['success'])
            return redirect(url_for(viewURL))
        elif 'error' in req:
            errorMessage(req['error'])

    elif function == 'unlock' and uuid != None:
        # Function kwargs
        req = unlockCrud(uuid=uuid)
        if 'success' in req:
            successMessage(req['success'])
            return redirect(url_for(viewURL))
        elif 'error' in req:
            errorMessage(req['error'])

    elif function == 'delete' and uuid != None:
        # Function kwargs
        req = deleteCrud(uuid=uuid)
        if 'success' in req:
            successMessage(req['success'])
            return redirect(url_for(viewURL))
        elif 'error' in req:
            errorMessage(req['error'])

    # Edit single row
    elif function == 'edit' and uuid != None:
        # Function kwargs
        kwargs = {'contentTitle': 'Edit {}'.format(viewName),
                  'submitStay': False}

        for r in putExecs:
            exec(r)

            if session['user_uuid'] == uuid:
                kwargs['noLocked'] = True

        if not 'Administrator' in session['roles']:
            if data.role == 'Administrator':
                errorMessage('You must have Administrator rights in order to edit another admin')
                return redirect(url_for('userBP.userView'))

        if putForm.validate_on_submit():
            if putForm.role.data != data.role:
                if data.contact == True:
                    errorMessage('You cannot change contact person roles')
                    return render_template(templateView, form=putForm, **kwargs)
                else:
                    putData['role'] = putForm.role.data
            else:
                putData['role'] = putForm.role.data


            req = putCrud(data=putData, uuid=uuid)
            if 'success' in req:
                successMessage(req['success'])
                return redirect(url_for(viewURL))
            elif 'error' in req:
                errorMessage(req['error'])

        return render_template(templateView, form=putForm, **kwargs)

@userBP.route('/group', methods=['GET'])
@userBP.route('/group/<string:function>', methods=['GET','POST'])
@userBP.route('/group/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def groupView(function=None, uuid=None):
    pass

#
## listView
#@userBP.route('/group', methods=['GET'])
#@userBP.route('/group/<string:function>', methods=['GET','POST'])
#@userBP.route('/group/<string:function>/<string:uuid>', methods=['GET','POST'])
#@loginRequired
#@requiredRole(['Administrator','Superuser'])
#def groupView(function=None, uuid=None):
#    kwargs = {'name':'User / Email groups'}
#
#    if function == None:
#        try:
#            groups = authAPI(endpoint='group?includeUsers=True', method='get', token=session['token'])['groups']
#
#            kwargs['tableData'] = [[g['uuid'], g['name'], g['desc'], len([u['uuid'] for u in g['users']])] for g in groups]
#        except:
#            pass
#        kwargs['tableColumns'] = ['Group name', 'Description','Users']
#
#    elif function == 'details':
#        try:
#            group = authAPI(endpoint='group/'+unicode(uuid)+'?includeUsers=True', method='get', token=session['token'])['group']
#            return render_template('user/groupDetails.html', group=group)
#        except:
#            errorMessage('Group info could not be fetched')
#
#    elif function == 'edit':
#        kwargs['contentTitle'] = 'Edit group'
#
#        group = authAPI(endpoint='group/'+unicode(uuid)+'?includeUsers=True', method='get', token=session['token'])['group']
#
#        users = authAPI(endpoint='user?includeRoles=True&includeGroups=True', method='get', token=session['token'])
#
#        form = groupForm(name=group['name'],
#                         desc=group['desc'],
#                         users=[g['uuid'] for g in group['users']])
#
#        if not 'error' in users:
#            users = users['users']
#            users = sorted(users, key=lambda k: k['name'])
#            form.users.choices = [(u['uuid'],u['name']+'  -  '+u['email']) for u in users]
#
#
#        if form.validate_on_submit():
#            dataDict = {'name': form.name.data,
#                        'desc':form.desc.data,
#                        'users':form.users.data}
#            req = authAPI(endpoint='group/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])
#
#            if not 'error' in req:
#                successMessage('Group has been modified')
#                return redirect(url_for('userBP.groupView'))
#            else:
#                errorMessage(req['error'])
#        return render_template('user/groupForm.html', form=form, **kwargs)
#
#    elif function == 'new':
#        kwargs['contentTitle'] = 'New Group'
#        users = authAPI(endpoint='user?includeRoles=True&includeGroups=True', method='get', token=session['token'])
#        form = groupForm()
#
#        if not 'error' in users:
#            users = users['users']
#            users = sorted(users, key=lambda k: k['name'])
#            form.users.choices = [(u['uuid'],u['name']+'  -  '+u['email']) for u in users]
#
#        if form.validate_on_submit():
#            dataDict = {'name': form.name.data,
#                        'desc':form.desc.data,
#                        'users':form.users.data}
#            req = authAPI(endpoint='group', method='post', dataDict=dataDict, token=session['token'])
#
#            if not 'error' in req:
#                successMessage('Group has been added')
#                return redirect(url_for('userBP.groupView'))
#            else:
#                errorMessage(req['error'])
#
#        return render_template('user/groupForm.html', form=form, **kwargs)
#    return render_template('listView.html', **kwargs)
