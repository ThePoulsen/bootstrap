from app import db
from flask import session
from app.masterData.models import status
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getStatuses():
    viewLog(table='status')
    return status.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getStatus(uuid):
    viewLog(table='status', uuid=unicode(uuid))
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
        postLog(table='status', uuid=unicode(row.uuid))
        return {'success': 'Status added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='status')
            return {'error': 'Status already exist'}
        else:
            errorLog(unicode(E), table='status')
            return {'error': unicode(E)}

def putStatus(data, uuid):
    row = getStatus(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='status', uuid=unicode(uuid), changes=changes)
        return {'success': 'Status updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='status')
            return {'error': 'Status already exist'}
        else:
            errorLog(unicode(E), table='status')
            return {'error': unicode(E)}

def deleteStatus(uuid):
    row = getStatus(uuid)
    try:
        db.session.delete(row)
        db.session.commit()
        deleteLog(table='status', uuid=unicode(uuid))
        return {'success': 'Status deleted'}
    except Exception as E:
        errorLog(unicode(E), table='status')
        return {'error': unicode(E)}

def statusSelectData():
    statuses = getStatuses()
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
