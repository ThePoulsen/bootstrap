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
    kwargs = {'title':'System users'}
    if function == 'details' and uuid != None:
        user = authAPI(endpoint='user/'+uuid+'?includeRoles=True&includeGroups=True', method='get', token=session['token'])
        if 'user' in user:
            return render_template('user/profile.html', user=user['user'])
        else:
            errorMessage('Your user profile is not found')
            return redirect(url_for('userBP.userView'))

    elif function == 'edit' and uuid != None:
        user = authAPI(endpoint='user/'+uuid+'?includeRoles=True&includeGroups=True', method='get', token=session['token'])
        print user
        if 'user' in user:
            if not 'Administrator' in session['roles']:
                if 'Administrator' in [r['title'] for r in user['user']['roles']]:
                    errorMessage('You must have Administrator rights in order to edit another admin')
                    return redirect(url_for('userBP.userView'))

            form = userForm(name=user['user']['name'],
                            email=user['user']['email'],
                            phone=user['user']['phone'])
            if user['user']['locked'] == True:
                form.locked.checked = True

            return render_template('user/userForm.html', form=form)
        else:
            errorMessage('User profile is not found')
            return redirect(url_for('userBP.userView'))

    elif function == 'delete' and uuid != None:
        return 'delete'

    elif function == 'new' and uuid == None:
        return 'new'

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
                temp = [u['uuid'],u['name'],u['email'], roles, groups, locked]
                tableData.append(temp)

            kwargs['tableColumns'] =['User name','Email','Roles','Groups', 'Locked?']
            kwargs['tableData'] = tableData
        else:
            errorMessage(users['error'])



    return render_template('listView.html', **kwargs)
