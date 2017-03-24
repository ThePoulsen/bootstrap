from app import db
from flask import session
from app.masterData.models import processArea
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getProcessAreas():
    viewLog(table='processArea')
    return processArea.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getProcessArea(uuid):
    viewLog(table='processArea', uuid=unicode(uuid))
    return processArea.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postProcessArea(data):
    row = processArea(title = data['title'],
                      desc = data['desc'],
                      tenant_uuid = session['tenant_uuid'],
                      uuid = UUID.uuid4(),
                      created=datetime.now(),
                      createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='processArea', uuid=unicode(row.uuid))
        return {'success': 'Process Area added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='processArea')
            return {'error': 'Process Area already exist'}
        else:
            errorLog(unicode(E), table='processArea')
            return {'error': unicode(E)}

def putProcessArea(data, uuid):
    row = getProcessArea(uuid)
    changes = compareDict(row=row, data=data)['modified']
    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='processArea', uuid=unicode(uuid), changes=changes)
        return {'success': 'Process Area updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='processArea')
            return {'error': 'Process Area already exist'}
        else:
            errorLog(unicode(E), table='processArea')
            return {'error': unicode(E)}

def deleteProcessArea(uuid):
    entry = getProcessArea(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        deleteLog(table='processArea', uuid=unicode(uuid))
        return {'success': 'Process Area deleted'}
    except Exception as E:
        errorLog(unicode(E), table='processArea')
        return {'error': unicode(E)}

def processAreaSelectData():
    data = getProcessAreas()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def processAreaListData():
    entries = getProcessAreas()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
