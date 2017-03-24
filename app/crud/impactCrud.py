from app import db
from flask import session
from app.masterData.models import impact
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getImpacts():
    viewLog(table='impact')
    return impact.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getImpact(uuid):
    viewLog(table='impact', uuid=unicode(uuid))
    return impact.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postImpact(data):
    row = impact(title = data['title'],
                   desc = data['desc'],
                   value = data['value'],
                   tenant_uuid = session['tenant_uuid'],
                   uuid = UUID.uuid4(),
                   created=datetime.now(),
                   createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='impact', uuid=unicode(row.uuid))
        return {'success': 'Impact added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='impact')
            return {'error': 'Impact already exist'}
        else:
            errorLog(unicode(E), table='impact')
            return {'error': unicode(E)}

def putImpact(data, uuid):
    row = getImpact(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.desc = data['desc']
    row.value = data['value']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='impact', uuid=unicode(uuid), changes=changes)
        return {'success': 'Impact updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='impact')
            return {'error': 'Impact already exist'}
        else:
            errorLog(unicode(E), table='impact')
            return {'error': unicode(E)}

def deleteImpact(uuid):
    entry = getImpact(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        deleteLog(table='impact', uuid=unicode(uuid))
        return {'success': 'Impact deleted'}
    except Exception as E:
        errorLog(unicode(E), table='impact')
        return {'error': unicode(E)}

def impactSelectData():
    data = getImpacts()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def impactListData():
    entries = getImpacts()
    data = []
    for r in entries:
        temp = [r.uuid, r.value, r.title, r.desc]
        data.append(temp)
    return data
