from app import db
from flask import session
from app.user.models import group, user
import uuid as UUID
from authAPI import authAPI
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

from app.services.services import compareDict
def getGroups():
    viewLog(table='group')
    return group.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getGroup(uuid):
    viewLog(table='group', uuid=unicode(uuid))
    return group.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postGroup(data):
    try:
        dataDict = {'name': data['title'],
                    'desc': data['desc'],
                    'users': data['users']}
        req = authAPI(endpoint='group', method='post', dataDict=dataDict, token=session['token'])
        if 'error' in req:
            return {'error': req['error']}

        else:
            try:
                grp = group(uuid = req['uuid'],
                            title=data['title'],
                            desc=data['desc'],
                            users=[user.query.filter_by(uuid=unicode(r)).first() for r in data['users']],
                            tenant_uuid=session['tenant_uuid'],
                            created=datetime.now(),
                            createdBy=session['user_uuid'])
                db.session.add(grp)
                db.session.commit()
                postLog(table='group', uuid=unicode(grp.uuid))
                return {'success': 'Group has been added'}
            except Exception as E:
                if 'unique constraint' in unicode(E):
                    errorLog('Unique constraint', table='group')
                    return {'error': 'Group already exist'}
                else:
                    errorLog(unicode(E), table='group')
                    return {'error': unicode(E)}

    except Exception as E:
        return {'error':unicode(E)}

def putGroup(data, uuid):
    try:
        dataDict = {'name': data['title'],
                    'desc': data['desc'],
                    'users': data['users']}

        req = authAPI(endpoint='group/'+unicode(uuid), method='put', dataDict=dataDict, token=session['token'])
        if 'error' in req:
            return {'error': req['error']}

        else:
            grp = getGroup(uuid)
            changes = compareDict(row=grp, data=data)['modified']

            try:
                currentUsers = [r.uuid for r in grp.users]
            except:
                currentUsers = []
            try:
                newUsers = [user.query.filter_by(uuid=unicode(r)).first().uuid for r in data['users']]
            except:
                newUsers = []

            if currentUsers != newUsers:
                changes['users'] = (currentUsers,newUsers)


            grp.title = data['title']
            grp.desc = data['desc']
            grp.users = [user.query.filter_by(uuid=unicode(r)).first() for r in data['users']]
            grp.modified = datetime.now()
            grp.modifiedBy = session['user_uuid']
            try:
                db.session.commit()
                putLog(table='group', uuid=unicode(uuid), changes=changes)
                return {'success': 'Group has been modified'}
            except Exception as E:
                if 'unique constraint' in unicode(E):
                    errorLog('Unique constraint', table='group')
                    return {'error': 'Group already exist'}
                else:
                    errorLog(unicode(E), table='group')
                    return {'error': unicode(E)}

    except Exception as E:
        return {'error': unicode(E)}

def deleteGroup(uuid):
    try:
        req = authAPI(endpoint='group/'+unicode(uuid), method='delete', token=session['token'])
        if 'error' in req:
            return {'error': req['error']}
        else:
            try:
                grp = getGroup(uuid)
                db.session.delete(grp)
                db.session.commit()
                deleteLog(table='group', uuid=unicode(uuid))
                return {'success': 'Group has been deleted'}
            except Exception as E:
                errorLog(unicode(E), table='group')
                return {'error': unicode(E)}

    except Exception as E:
        errorLog(unicode(E), table='group')
        return {'error': unicode(E)}

def groupSelectData():
    data = getGroups()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def groupListData():
    data = getGroups()
    output = []
    for r in data:
        users = [u.name+' - '+u.email for u in r.users]
        temp = [r.uuid, r.title, r.desc, users]
        output.append(temp)
    return output
