from app import db
from flask import session
from app.user.models import user, group
from datetime import datetime
from authAPI import authAPI

def getUsers():
    return user.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getUser(uuid):
    return user.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postUser(data):
    dataDict = {'name': data.name.data,
                'email': data.email.data,
                'phone': data.phone.data,
                'groups': data.groups.data}
    dataDict['roles'] = [data.role.data]

    req = authAPI('user', method='post', dataDict=dataDict, token=session['token'])

    if 'success' in req:
        usr = user(uuid = req['uuid'],
                   initials = data['initials'],
                   name = data['name'],
                   email = data['email'],
                   phone = data['phone'],
                   role = data['role'],
                   active = True,
                   locked = False,
                   contact = data['contact'],
                   confirmed = False,
                   created=datetime.now(),
                   createdBy=session['user_uuid'],
                   groups=[group.query.filter_by(uuid=unicode(r)).first() for r in data['groups']])

        try:
            db.session.add(usr)
            db.session.commit()
            return {'success': 'User has been added'}
        except Exception as E:
            if 'unique constraint' in unicode(E):
                return {'error': 'User already exist'}
            else:
                return {'error': unicode(E)}
    else:
        return {'error': req['error']}

def confirmUser(uuid):
    usr = getUser(uuid)
    usr.locked = True

def putUser(data, uuid):
    usr = getUser(uuid)

    usr.initials = data['initials']
    usr.name = data['name']
    usr.email = data['email']
    usr.phone = data['phone']
    usr.role = data['role']
    usr.modified = datetime.now()
    usr.modifiedBy = session['user_uuid']

def deactivateUser(uuid):
    usr = getUser(uuid)
    usr.active = False

def activateUser(uuid):
    usr = getUser(uuid)
    usr.active = True

def lockUser(uuid):
    usr = getUser(uuid)
    usr.locked = True

def unlockUser(uuid):
    usr = getUser(uuid)
    usr.locked = False

def setContactUser(uuid):
    usr = getUser(uuid)
    usr.locked = True

def removeContactUser(uuid):
    usr = getUser(uuid)
    usr.locked = False

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
        temp = [r.uuid, r.name, r.email, r.role, '', r.locked, r.contact, r.active, r.confirmed]
        data.append(temp)
    return data
