from app import db
from flask import session
from app.masterData.models import status
import uuid as UUID
from datetime import datetime

def getStatuses():
    return status.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getStatus(uuid):
    return status.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postStatus(data):
    row = status(title = data['title'],
                 tenant_uuid = session['tenant_uuid'],
                 uuid = UUID.uuid4(),
                 created=datetime.now(),
                 createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Status added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Status already exist'}
        else:
            return {'error': unicode(E)}

def putStatus(data, uuid):
    r = getStatus(uuid)

    r.title = data['title']
    r.modified = datetime.now()
    r.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Status updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Status already exist'}
        else:
            return {'error': unicode(E)}

def deleteStatus(uuid):
    r = getStatusn(uuid)
    try:
        db.session.delete(r)
        db.session.commit()
        return {'success': 'Status deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def statusSelectData():
    statuses = status.query.filter_by(tenant_uuid=session['tenant_uuid']).all()
    dataList = []
    for s in statuses:
        dataList.append((s.uuid, s.title))
    return dataList

def statusListData():
    statuses = getStatuses()
    data = []
    for s in statuses:
        temp = [s.uuid, s.title]
        data.append(temp)
    return data
