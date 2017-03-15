## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for
from authAPI import authAPI
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, sendMail
from forms import userForm
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

# listView
@userBP.route('/user', methods=['GET'])
@userBP.route('/user/<string:function>', methods=['GET','POST'])
@userBP.route('/user/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def userView(function=None, uuid=None):
    kwargs = {'title':'System users',
              'function':unicode(function)}
    if function == 'details' and uuid != None:
        user = authAPI(endpoint='user/'+uuid+'?includeRoles=True&includeGroups=True', method='get', token=session['token'])
        if 'user' in user:
            return render_template('user/profile.html', user=user['user'])
        else:
            errorMessage('Your user profile is not found')
            return redirect(url_for('userBP.userView'))

    elif function == 'edit' and uuid != None:
        user = authAPI(endpoint='user/'+uuid+'?includeRoles=True&includeGroups=True', method='get', token=session['token'])
        if 'user' in user:
            if not 'Administrator' in session['roles']:
                if 'Administrator' in [r['title'] for r in user['user']['roles']]:
                    errorMessage('You must have Administrator rights in order to edit another admin')
                    return redirect(url_for('userBP.userView'))

            roles = [r['title'] for r in user['user']['roles']]
            if 'User' in roles:
                role = 'User'
            elif 'Superuser' in roles:
                role = 'Superuser'
            elif 'Administrator' in roles:
                role = 'Administrator'

            if user['user']['locked'] == True:
                locked = 'Locked'
            else:
                locked = 'Unlocked'

            form = userForm(name=user['user']['name'],
                            email=user['user']['email'],
                            phone=user['user']['phone'],
                            role=role,
                            locked=locked)


            if form.validate_on_submit() and request.method == 'POST':

                dataDict = {'name': form.name.data,
                            'email': form.email.data,
                            'phone': form.phone.data}
                dataDict['roles'] = [form.role.data]
                dataDict['groups'] = []

                if form.role.data != role:
                    if user['user']['isContact'] == True:
                        errorMessage('You cannot change contact person roles')

                else:

                    if form.locked.data != locked:
                        if form.locked.data == 'Locked':
                            lockUser = authAPI(endpoint='lockUser/'+unicode(uuid), method='put', token=session['token'])
                        else:
                            lockUser = authAPI(endpoint='unlockUser/'+unicode(uuid), method='put', token=session['token'])

                        if 'success' in lockUser:
                            pass
                        elif 'error' in lockUser:
                            errorMessage(lockUser['error'])

                    updateUser = authAPI(endpoint='user/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])
                    if not 'error' in updateUser:
                        successMessage(unicode(updateUser['success']))
                        return redirect(url_for('userBP.userView'))
                    else:
                        errorMessage(unicode(updateUser['error']))

            return render_template('user/userForm.html', form=form)
        else:
            errorMessage('User profile is not found')
            return redirect(url_for('userBP.userView'))

    elif function == 'delete' and uuid != None:
        return 'delete'

    elif function == 'new' and uuid == None:

        form = userForm(role='User',
                        locked='Unlocked')

        if form.validate_on_submit():
            dataDict = {'name': form.name.data,
                        'email': form.email.data,
                        'phone': form.phone.data}

            dataDict['roles'] = [form.role.data]
            dataDict['groups'] = []
            return unicode(dataDict)

        return render_template('user/userForm.html', form=form, **kwargs)

    # Get users
    elif function == None:
        users = authAPI(endpoint='user?includeRoles=True&includeGroups=True', method='get', token=session['token'])

        if not 'error' in users:
            users = users['users']
            tableData = []
            for u in users:
                roles = ''
                for r in u['roles']:
                    roles = roles + str(r['title']) +'<br>'
                groups = ''
                for gr in u['groups']:
                    groups = groups + str(gr['name']) +'<br>'
                if u['locked']:
                    locked = '<i class="fa fa-lock"></i>'
                else:
                    locked= '<i class="fa fa-unlock"></i>'
                if u['isContact']:
                    contact = '<i class="fa fa-check"></i>'
                else:
                    contact = '<i class="fa fa-minus"></i>'

                temp = [u['uuid'],u['name'],u['email'], roles, groups, locked, contact]
                tableData.append(temp)

            kwargs['tableColumns'] =['User name','Email','Roles','Groups', 'Locked?', 'Contact?']
            kwargs['tableData'] = tableData
        else:
            errorMessage(users['error'])



    return render_template('listView.html', **kwargs)
