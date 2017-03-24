from app import db
from flask import session
from app.masterData.models import riskResponse
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getRiskResponses():
    viewLog(table='riskResponse')
    return riskResponse.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRiskResponse(uuid):
    viewLog(table='riskResponse', uuid=unicode(uuid))
    return riskResponse.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRiskResponse(data):
    row = riskResponse(title = data['title'],
                       desc = data['desc'],
                       tenant_uuid = session['tenant_uuid'],
                       uuid = UUID.uuid4(),
                       created=datetime.now(),
                       createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='riskResponse', uuid=unicode(row.uuid))
        return {'success': 'Risk Response added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='riskResponse')
            return {'error': 'Risk Response already exist'}
        else:
            errorLog(unicode(E), table='riskResponse')
            return {'error': unicode(E)}

def putRiskResponse(data, uuid):
    row = getRiskResponse(uuid)
    changes = compareDict(row=row, data=data)['modified']

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='riskResponse', uuid=unicode(uuid), changes=changes)
        return {'success': 'Risk Response updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='riskResponse')
            return {'error': 'Risk Response already exist'}
        else:
            errorLog(unicode(E), table='riskResponse')
            return {'error': unicode(E)}

def deleteRiskResponse(uuid):
    entry = getRiskResponse(uuid)
    if entry.treatments:
        return {'error': 'Risk Response cannot be deleted as long as there are Treatments assigned this Risk Response'}
    try:
        db.session.delete(entry)
        db.session.commit()
        deleteLog(table='riskResponse', uuid=unicode(uuid))
        return {'success': 'Risk Response deleted'}
    except Exception as E:
        errorLog(unicode(E), table='riskResponse')
        return {'error': unicode(E)}

def riskResponseSelectData():
    data = getRiskResponses()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def riskResponseListData():
    entries = getRiskResponses()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
