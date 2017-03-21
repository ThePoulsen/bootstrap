from app import db
from flask import session
from app.user.models import user, group
from datetime import datetime
from authAPI import authAPI
import os
from app.services.services import sendMail

def getUsers():
    return user.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getUser(uuid):
    return user.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postUser(data):
    if not 'tenant_uuid' in session:
        tenant_uuid = data['tenant_uuid']
    else:
        tenant_uuid = session['tenant_uuid']

    try:
        user.query.filter_by(tenant_uuid=tenant_uuid, email=data['email']).first().name
        return {'error': 'User already exist'}

    except:
        dataDict = {'name': data['name'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'groups': data['groups']}
        dataDict['roles'] = [data['role']]
        req = authAPI('user', method='post', dataDict=dataDict, token=session['token'])

        if 'error' in req:
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
            try:
                db.session.add(usr)
                db.session.commit()
                return {'success': 'User has been added'}
            except Exception as E:
                if 'unique constraint' in unicode(E):
                    return {'error': 'User already exist'}
                else:
                    return {'error': unicode(E)}

def confirmUser(uuid):
    usr = getUser(uuid)
    usr.confirmed = True
    db.session.commit()

def putUser(data, uuid):
    usr = getUser(uuid)

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
            return {'success':'User has been modified'}
        else:
            return {'error':req['error']}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'User already exist'}
        else:
            return {'error': unicode(E)}

def deactivateUser(uuid):
    usr = getUser(uuid)
    usr.active = False
    db.session.commit()

def activateUser(uuid):
    usr = getUser(uuid)
    usr.active = True
    db.session.commit()

def lockUser(uuid):
    usr = getUser(uuid)
    usr.locked = True
    db.session.commit()

def unlockUser(uuid):
    usr = getUser(uuid)
    usr.locked = False
    db.session.commit()

def setContactUser(uuid):
    usr = getUser(uuid)
    usr.locked = True
    db.session.commit()

def removeContactUser(uuid):
    usr = getUser(uuid)
    usr.locked = False
    db.session.commit()

def userSelectData():
    data = getUsers()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def userListData():
    data = getUsers()
    output = []
    for r in data:
        if r.locked == True:
            locked = '<i class="fa fa-check" aria-hidden="true"></i>'
        else:
            locked = '<i class="fa fa-minus" aria-hidden="true"></i>'

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


        temp = [r.uuid,r.initials, r.name, r.email, r.role, '', locked, contact, active, confirmed]
        output.append(temp)
    return output
