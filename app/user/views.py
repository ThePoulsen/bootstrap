## -*- coding: utf-8 -*-

from flask import render_template, Blueprint, flash, request, session, redirect, url_for, jsonify
from authAPI import authAPI
from app.services.services import errorMessage, successMessage, loginRequired, requiredRole, sendMail
from forms import userForm, groupForm
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
              'noLocked':False}

    if function == 'details' and uuid != None:
        user = authAPI(endpoint='user/'+uuid+'?includeRoles=True&includeGroups=True', method='get', token=session['token'])
        if 'user' in user:
            return render_template('user/profile.html', user=user['user'])
        else:
            errorMessage('Your user profile is not found')
            return redirect(url_for('userBP.userView'))

    elif function == 'edit' and uuid != None:
        user = authAPI(endpoint='user/'+uuid+'?includeRoles=True&includeGroups=True', method='get', token=session['token'])
        kwargs['contentTitle'] = 'Edit User'

        groups = authAPI(endpoint='group', method='get', token=session['token'])

        if 'groups' in groups:
            groups = [(g['uuid'], g['name']) for g in groups['groups']]
        else:
            groups = []

        if 'user' in user:
            if not 'Administrator' in session['roles']:
                if 'Administrator' in [r['title'] for r in user['user']['roles']]:
                    errorMessage('You must have Administrator rights in order to edit another admin')
                    return redirect(url_for('userBP.userView'))

            if session['user_uuid'] == uuid:
                kwargs['noLocked'] = True

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
                            role=role, locked=locked,
                            groups = [g['uuid'] for g in user['user']['groups']])

            form.groups.choices = groups

            if form.validate_on_submit():
                dataDict = {'name': form.name.data,
                            'email': form.email.data,
                            'phone': form.phone.data,
                            'groups': form.groups.data}

                if form.locked.data != locked:
                    if form.locked.data == 'Locked':
                        lockUser = authAPI(endpoint='lockUser/'+unicode(uuid), method='put', token=session['token'])
                    else:
                        lockUser = authAPI(endpoint='unlockUser/'+unicode(uuid), method='put', token=session['token'])

                    if 'error' in lockUser:
                        errorMessage(lockUser['error'])


                if form.role.data != role:
                    if user['user']['isContact'] == True:
                        errorMessage('You cannot change contact person roles')
                        return render_template('user/userForm.html', form=form, **kwargs)
                    else:
                        dataDict['roles'] = [form.role.data]
                else:
                    dataDict['roles'] = [form.role.data]


                updateUser = authAPI(endpoint='user/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])

                if not 'error' in updateUser:
                    successMessage(unicode(updateUser['success']))
                    return redirect(url_for('userBP.userView'))
                else:
                    errorMessage(unicode(updateUser['error']))

            return render_template('user/userForm.html', form=form, **kwargs)
        else:
            errorMessage('User profile is not found')
            return redirect(url_for('userBP.userView'))

    elif function == 'delete' and uuid != None:
        req = authAPI(endpoint='user/'+unicode(uuid), method='delete', token=session['token'])
        if 'success' in req:
            successMessage('User has been deleted')
            return redirect(url_for('userBP.userView'))
        elif 'error' in req:
            errorMessage(req['error'])
            return redirect(url_for('userBP.userView'))

    elif function == 'new' and uuid == None:
        kwargs['noLocked'] = True
        kwargs['contentTitle'] = 'New User'

        groups = authAPI(endpoint='group', method='get', token=session['token'])

        if 'groups' in groups:
            groups = [(g['uuid'], g['name']) for g in groups['groups']]
        else:
            groups = []

        form = userForm(role='User',
                        locked='Unlocked')

        form.groups.choices = groups

        if form.validate_on_submit():
            dataDict = {'name': form.name.data,
                        'email': form.email.data,
                        'phone': form.phone.data,
                        'groups': form.groups.data}
            dataDict['roles'] = [form.role.data]

            req = authAPI('user', method='post', dataDict=dataDict, token=session['token'])

            if 'error' in req:
                errorMessage(req['error'])

            elif 'success' in req:
                # send email confirmation
                if os.environ['sendMail'] == 'True':
                    subject = u'Please confirm your account'
                    tok = req['token']
                    email = form.email.data
                    confirm_url = url_for('authBP.confirmEmailView',token=tok, _external=True)
                    html = render_template('email/verify.html', confirm_url=confirm_url)

                    sendMail(subject=subject,
                             sender=os.environ['mailSender'],
                             recipients=[email],
                             html_body=html,
                             text_body = None)

                successMessage('User has been added')
                return redirect(url_for('userBP.userView'))

        return render_template('user/userForm.html', form=form, **kwargs)

    elif function == None:
        users = authAPI(endpoint='user?includeRoles=True&includeGroups=True', method='get', token=session['token'])

#        return jsonify(users)

        if not 'error' in users:
            users = users['users']
            users = sorted(users, key=lambda k: k['name'])
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

# listView
@userBP.route('/group', methods=['GET'])
@userBP.route('/group/<string:function>', methods=['GET','POST'])
@userBP.route('/group/<string:function>/<string:uuid>', methods=['GET','POST'])
@loginRequired
@requiredRole(['Administrator','Superuser'])
def groupView(function=None, uuid=None):
    kwargs = {'name':'User / Email groups'}

    if function == None:
        try:
            groups = authAPI(endpoint='group?includeUsers=True', method='get', token=session['token'])['groups']

            kwargs['tableData'] = [[g['uuid'], g['name'], g['desc'], len([u['uuid'] for u in g['users']])] for g in groups]
        except:
            pass
        kwargs['tableColumns'] = ['Group name', 'Description','Users']

    elif function == 'details':
        try:
            group = authAPI(endpoint='group/'+unicode(uuid)+'?includeUsers=True', method='get', token=session['token'])['group']
            return render_template('user/groupDetails.html', group=group)
        except:
            errorMessage('Group info could not be fetched')

    elif function == 'edit':
        kwargs['contentTitle'] = 'Edit group'

        group = authAPI(endpoint='group/'+unicode(uuid)+'?includeUsers=True', method='get', token=session['token'])['group']

        users = authAPI(endpoint='user?includeRoles=True&includeGroups=True', method='get', token=session['token'])

        form = groupForm(name=group['name'],
                         desc=group['desc'],
                         users=[g['uuid'] for g in group['users']])

        if not 'error' in users:
            users = users['users']
            users = sorted(users, key=lambda k: k['name'])
            form.users.choices = [(u['uuid'],u['name']+'  -  '+u['email']) for u in users]


        if form.validate_on_submit():
            dataDict = {'name': form.name.data,
                        'desc':form.desc.data,
                        'users':form.users.data}
            req = authAPI(endpoint='group/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])

            if not 'error' in req:
                successMessage('Group has been modified')
                return redirect(url_for('userBP.groupView'))
            else:
                errorMessage(req['error'])
        return render_template('user/groupForm.html', form=form, **kwargs)

    elif function == 'new':
        kwargs['contentTitle'] = 'New Group'
        users = authAPI(endpoint='user?includeRoles=True&includeGroups=True', method='get', token=session['token'])
        form = groupForm()

        if not 'error' in users:
            users = users['users']
            users = sorted(users, key=lambda k: k['name'])
            form.users.choices = [(u['uuid'],u['name']+'  -  '+u['email']) for u in users]

        if form.validate_on_submit():
            dataDict = {'name': form.name.data,
                        'desc':form.desc.data,
                        'users':form.users.data}
            req = authAPI(endpoint='group', method='post', dataDict=dataDict, token=session['token'])

            if not 'error' in req:
                successMessage('Group has been added')
                return redirect(url_for('userBP.groupView'))
            else:
                errorMessage(req['error'])

        return render_template('user/groupForm.html', form=form, **kwargs)
    return render_template('listView.html', **kwargs)
