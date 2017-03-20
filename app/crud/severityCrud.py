from app import db
from flask import session
from app.masterData.models import severity
import uuid as UUID
from datetime import datetime

def getSeverities():
    return severity.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getSeverity(uuid):
    return severity.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postSeverity(data):
    row = severity(title = data['title'],
                   desc = data['desc'],
                   value = data['value'],
                   tenant_uuid = session['tenant_uuid'],
                   uuid = UUID.uuid4(),
                   created=datetime.now(),
                   createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Severity added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Severity already exist'}
        else:
            return {'error': unicode(E)}

def putSeverity(data, uuid):
    row = getSeverity(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.value = data['value']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Severity updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Severity already exist'}
        else:
            return {'error': unicode(E)}

def deleteSeverity(uuid):
    entry = getSeverity(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Severity deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def severitySelectData():
    data = getSeverities()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def severityListData():
    entries = getSeverities()
    data = []
    for r in entries:
        temp = [r.uuid, r.value, r.title, r.desc]
        data.append(temp)
    return data
