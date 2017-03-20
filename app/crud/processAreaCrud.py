from app import db
from flask import session
from app.masterData.models import processArea
import uuid as UUID
from datetime import datetime

def getProcessAreas():
    return processArea.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getProcessArea(uuid):
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
        return {'success': 'Process Area added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Process Area already exist'}
        else:
            return {'error': unicode(E)}

def putProcessArea(data, uuid):
    row = getProcessArea(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Process Area updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Process Area already exist'}
        else:
            return {'error': unicode(E)}

def deleteProcessArea(uuid):
    entry = getProcessArea(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Process Area deleted'}
    except Exception as E:
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
