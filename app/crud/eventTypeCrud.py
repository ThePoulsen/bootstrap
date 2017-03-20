from app import db
from flask import session
from app.masterData.models import eventType
import uuid as UUID
from datetime import datetime

def getsEventType():
    return eventType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getEventType(uuid):
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
        return {'success': 'Event Type added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Event Type already exist'}
        else:
            return {'error': unicode(E)}

def putEventType(data, uuid):
    row = getEventType(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Event Type updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Event Type already exist'}
        else:
            return {'error': unicode(E)}

def deleteEventType(uuid):
    entry = getEventType(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Event Type deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def eventTypeSelectData():
    data = getsEventType()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def eventTypeListData():
    entries = getsEventType()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
