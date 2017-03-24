from app import db
from flask import session, url_for, render_template
from app.user.models import user, group
from datetime import datetime
from authAPI import authAPI
import os
from app.services.services import sendMail
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getUsers():
    viewLog(table='user')
    return user.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getUser(uuid):
    viewLog(table='user', uuid=unicode(uuid))
    return user.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postUser(data):
    if not 'tenant_uuid' in session:
        tenant_uuid = data['tenant_uuid']
    else:
        tenant_uuid = session['tenant_uuid']

    try:
        user.query.filter_by(tenant_uuid=tenant_uuid, email=data['email']).first().name
        errorLog('Unique constraint', table='user')
        return {'error': 'User already exist'}

    except:
        dataDict = {'name': data['name'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'groups': data['groups']}
        dataDict['roles'] = [data['role']]
        req = authAPI('user', method='post', dataDict=dataDict, token=session['token'])

        if 'error' in req:
            errorLog(req['error'], table='user')
            return {'error': req['error']}

        else:
            usr = user(uuid = req['user_uuid'],
                       initials = data['initials'],
                       name = data['name'],
                       email = data['email'],
                       phone = data['phone'],
                       role = data['role'],
                       active = True,
                       locked = False,
                       tenant_uuid = tenant_uuid,
                       contact = data['contact'],
                       confirmed = False,
                       created=datetime.now(),
                       createdBy=session['user_uuid'],
                       groups=[group.query.filter_by(uuid=unicode(r)).first() for r in data['groups']])

            # send email confirmation
            if os.environ['sendMail'] == 'True':
                try:
                    subject = u'Please confirm your account'
                    tok = req['token']
                    email = data['email']
                    confirm_url = url_for('authBP.confirmEmailView',token=tok, _external=True)
                    html = render_template('email/verify.html', confirm_url=confirm_url)

                    sendMail(subject=subject,
                             sender=os.environ['mailSender'],
                             recipients=[email],
                             html_body=html,
                             text_body = None)
                except Exception as E:
                    print E
            try:
                db.session.add(usr)
                db.session.commit()
                postLog(table='user', uuid=unicode(row.uuid))
                return {'success': 'User has been added'}
            except Exception as E:
                if 'unique constraint' in unicode(E):
                    errorLog('Unique constraint', table='user')
                    return {'error': 'User already exist'}
                else:
                    errorLog(unicode(E), table='user')
                    return {'error': unicode(E)}

def confirmUser(uuid, tenant_uuid):
    try:
        usr = user.query.filter_by(uuid=uuid, tenant_uuid=tenant_uuid).first()
        usr.confirmed = True
        db.session.commit()
        logEntry('User confirmed: {}'.format(usr.uuid), table='user')
        return {'success':'User confirmed'}
    except Exception as E:
        errorLog(unicode(E), table='user')
        return {'error':unicode(E)}

def putUser(data, uuid):
    usr = getUser(uuid)
    changes = compareDict(row=row, data=data)['modified']

    try:
        currentGroups = [r.uuid for r in usr.groups]
    except:
        currentGroups = []
    try:
        newGroups = [group.query.filter_by(uuid=unicode(r)).first().uuid for r in data['groups']]
    except:
        newGroups = []

    if currentGroups != newGroups:
        changes['groups'] = (currentGroups,newGroups)

    usr.groups = [group.query.filter_by(uuid=unicode(r)).first() for r in data['groups']]
    usr.initials = data['initials']
    usr.name = data['name']
    usr.email = data['email']
    usr.phone = data['phone']
    usr.role = data['role']
    usr.modified = datetime.now()
    usr.modifiedBy = session['user_uuid']


    dataDict = {'name': data['name'],
                'email': data['email'],
                'phone': data['phone'],
                'groups': data['groups'],
                'roles': [data['role']]}
    try:
        db.session.add(usr)
        db.session.commit()
        req = authAPI(endpoint='user/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])

        if not 'error' in req:
            putLog(table='user', uuid=unicode(uuid), changes=changes)
            return {'success':'User has been modified'}
        else:
            errorLog(req['error'], table='user')
            return {'error':req['error']}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='user')
            return {'error': 'User already exist'}
        else:
            errorLog(unicode(E), table='user')
            return {'error': unicode(E)}

def deactivateUser(uuid):
    try:
        usr = getUser(uuid)
        usr.active = False
        db.session.commit()
        logEntry('User deactivated: {}'.format(usr.uuid), table='user')
        return {'success': 'User has been deactivated'}
    except Exception as E:
        errorLog(unicode(E), table='user')
        return {'error':unicode(E)}

def activateUser(uuid):
    try:
        usr = getUser(uuid)
        usr.active = True
        db.session.commit()
        logEntry('User activated: {}'.format(usr.uuid), table='user')
        return {'success': 'User has been activated'}
    except Exception as E:
        errorLog(unicode(E), table='user')
        return {'error':unicode(E)}

def deleteUser(uuid):
    try:
        usr = getUser(uuid)
        req = authAPI(endpoint='user/'+unicode(uuid), method='delete', token=session['token'])
        if 'success' in req:
            try:
                db.session.delete(usr)
                db.session.commit()
                deleteLog(table='user', uuid=unicode(uuid))
                return {'success': 'User has been activated'}
            except Exception as E:
                errorLog(unicode(E), table='user')
                return {'error':unicode(E)}
        else:
            errorLog(req['error'], table='user')
            return {'error':req['error']}
    except Exception as E:
        errorLog(unicode(E), table='user')
        return {'error':unicode(E)}

def lockUser(uuid):
    try:
        usr = getUser(uuid)
        req = authAPI(endpoint='lockUser/'+unicode(uuid), method='put', token=session['token'])
        if 'success' in req:
            try:
                usr.locked = True
                db.session.commit()
                logEntry('User locked: {}'.format(usr.uuid), table='user')
                return {'success': 'User has been locked out of the system'}
            except Exception as E:
                errorLog(unicode(E), table='user')
                return {'error':unicode(E)}
        else:
            errorLog(req['error'], table='user')
            return {'error': req['error']}
    except Exception as E:
        errorLog(unicode(E), table='user')
        return {'error':unicode(E)}

def unlockUser(uuid):
    try:
        usr = getUser(uuid)
        req = authAPI(endpoint='unlockUser/'+unicode(uuid), method='put', token=session['token'])
        if 'success' in req:
            try:
                usr.locked = False
                db.session.commit()
                logEntry('User unlocked: {}'.format(usr.uuid), table='user')
                return {'success': 'User can now use the system again'}
            except Exception as E:
                errorLog(unicode(E), table='user')
                return {'error':unicode(E)}
        else:
            errorLog(req['error'], table='user')
            return {'error': req['error']}
    except Exception as E:
        errorLog(unicode(E), table='user')
        return {'error':unicode(E)}

def setContactUser(uuid):
    usr = getUser(uuid)
    usr.locked = True
    logEntry('User now contact: {}'.format(usr.uuid), table='user')
    db.session.commit()

def removeContactUser(uuid):
    usr = getUser(uuid)
    usr.locked = False
    logEntry('User no longer contact: {}'.format(usr.uuid), table='user')
    db.session.commit()

def userSelectData():
    data = getUsers()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.name))
    return dataList

def userListData():
    data = getUsers()
    output = []
    for r in data:
        if r.locked == 'true':
            locked = '<i class="fa fa-lock" aria-hidden="true"></i>'
        else:
            locked = '<i class="fa fa-unlock" aria-hidden="true"></i>'

        if r.contact == True:
            contact = '<i class="fa fa-check" aria-hidden="true"></i>'
        else:
            contact = '<i class="fa fa-minus" aria-hidden="true"></i>'

        if r.active == True:
            active = '<i class="fa fa-check" aria-hidden="true"></i>'
        else:
            active = '<i class="fa fa-minus" aria-hidden="true"></i>'

        if r.confirmed == True:
            confirmed = '<i class="fa fa-check" aria-hidden="true"></i>'
        else:
            confirmed = '<i class="fa fa-minus" aria-hidden="true"></i>'

        groups = [g.title for g in r.groups]

        temp = [r.uuid,r.initials, r.name, r.email, r.role, groups, locked, contact, active, confirmed]
        output.append(temp)
    return output
