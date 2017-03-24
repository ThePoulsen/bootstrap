from app import db
from flask import session
from app.masterData.models import eventType
import uuid as UUID
from datetime import datetime
from app.audit.services import logEntry, viewLog, postLog, deleteLog, putLog, errorLog
from app.services.services import compareDict

def getsEventType():
    viewLog(table='eventType')
    return eventType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getEventType(uuid):
    viewLog(table='eventType', uuid=unicode(uuid))
    return eventType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postEventType(data):
    row = eventType(title = data['title'],
                    desc = data['desc'],
                    tenant_uuid = session['tenant_uuid'],
                    uuid = UUID.uuid4(),
                    created=datetime.now(),
                    createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        postLog(table='eventType', uuid=unicode(row.uuid))
        return {'success': 'Event Type added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='eventType')
            return {'error': 'Event Type already exist'}
        else:
            errorLog(unicode(E), table='eventType')
            return {'error': unicode(E)}

def putEventType(data, uuid):
    row = getEventType(uuid)
    changes = compareDict(row=row, data=data)['modified']

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        putLog(table='eventType', uuid=unicode(uuid), changes=changes)
        return {'success': 'Event Type updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            errorLog('Unique constraint', table='eventType')
            return {'error': 'Event Type already exist'}
        else:
            errorLog(unicode(E), table='eventType')
            return {'error': unicode(E)}

def deleteEventType(uuid):
    row = getEventType(uuid)
    try:
        db.session.delete(row)
        db.session.commit()
        deleteLog(table='eventType', uuid=unicode(uuid))
        return {'success': 'Event Type deleted'}
    except Exception as E:
        errorLog(unicode(E), table='eventType')
        return {'error': unicode(E)}

def eventTypeSelectData():
    rows = getsEventTypes()
    dataList = []
    for r in rows:
        dataList.append((r.uuid, r.title))
    return dataList

def eventTypeListData():
    rows = getsEventTypes()
    data = []
    for r in rows:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
