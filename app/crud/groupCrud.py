from app import db
from flask import session
from app.user.models import group, user
import uuid as UUID
from authAPI import authAPI
from datetime import datetime

def getGroups():
    return group.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getGroup(uuid):
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
                return {'success': 'Group has been added'}
            except Exception as E:
                if 'unique constraint' in unicode(E):
                    return {'error': 'Group already exist'}
                else:
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
            grp.title = data['title']
            grp.desc = data['desc']
            grp.users = [user.query.filter_by(uuid=unicode(r)).first() for r in data['users']]
            grp.modified = datetime.now()
            grp.modifiedBy = session['user_uuid']
            try:
                db.session.commit()
                return {'success': 'Group has been modified'}
            except Exception as E:
                if 'unique constraint' in unicode(E):
                    return {'error': 'Group already exist'}
                else:
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
                return {'success': 'Group has been deleted'}
            except Exception as E:
                if 'unique constraint' in unicode(E):
                    return {'error': 'Group already exist'}
                else:
                    return {'error': unicode(E)}

    except Exception as E:
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
