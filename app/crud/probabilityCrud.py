from app import db
from flask import session
from app.masterData.models import probability
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getProbabilities():
    viewLog(table='probability')
    return probability.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getProbability(uuid):
    viewLog(table='probability', uuid=unicode(uuid))
    return probability.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postProbability(data):
    row = probability(title = data['title'],
                     desc = data['desc'],
                     value = data['value'],
                     tenant_uuid = session['tenant_uuid'],
                     uuid = UUID.uuid4(),
                     created=datetime.now(),
                     createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='probability', uuid=unicode(row.uuid))
        return {'success': 'Probability added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='probability')
            return {'error': 'Probability already exist'}
        else:
            errorLog(unicode(E), table='probability')
            return {'error': unicode(E)}

def putProbability(data, uuid):
    row = getProbability(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.desc = data['desc']
    row.value = data['value']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='probability', uuid=unicode(uuid), changes=changes)
        return {'success': 'Probability updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='probability')
            return {'error': 'Probability already exist'}
        else:
            errorLog(unicode(E), table='probability')
            return {'error': unicode(E)}

def deleteProbability(uuid):
    entry = getProbability(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        deleteLog(table='probability', uuid=unicode(uuid))
        return {'success': 'Probability deleted'}
    except Exception as E:
        errorLog(unicode(E), table='probability')
        return {'error': unicode(E)}

def probabilitySelectData():
    data = getProbabilities()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def probabilityListData():
    entries = getProbabilities()
    data = []
    for r in entries:
        temp = [r.uuid, r.value, r.title, r.desc]
        data.append(temp)
    return data
