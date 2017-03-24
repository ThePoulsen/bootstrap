from app import db
from flask import session
from app.masterData.models import riskArea
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getRiskAreas():
    viewLog(table='riskArea')
    return riskArea.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRiskArea(uuid):
    viewLog(table='riskArea', uuid=unicode(uuid))
    return riskArea.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRiskArea(data):
    row = riskArea(title = data['title'],
                   desc = data['desc'],
                   tenant_uuid = session['tenant_uuid'],
                   uuid = UUID.uuid4(),
                   created=datetime.now(),
                   createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='riskArea', uuid=unicode(row.uuid))
        return {'success': 'Risk Area added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='riskArea')
            return {'error': 'Risk Area already exist'}
        else:
            errorLog(unicode(E), table='riskArea')
            return {'error': unicode(E)}

def putRiskArea(data, uuid):
    row = getRiskArea(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='riskArea', uuid=unicode(uuid), changes=changes)
        return {'success': 'Risk Area updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='riskArea')
            return {'error': 'Risk Area already exist'}
        else:
            errorLog(unicode(E), table='riskArea')
            return {'error': unicode(E)}

def deleteRiskArea(uuid):
    entry = getRiskArea(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        deleteLog(table='riskArea', uuid=unicode(uuid))
        return {'success': 'Risk Area deleted'}
    except Exception as E:
        errorLog(unicode(E), table='riskArea')
        return {'error': unicode(E)}

def riskAreaSelectData():
    data = getRiskAreas()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def riskAreaListData():
    entries = getRiskAreas()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
