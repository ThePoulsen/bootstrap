from app import db
from flask import session
from app.masterData.models import riskType
import uuid as UUID
from datetime import datetime

def getRiskTypes():
    return riskType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getRiskType(uuid):
    return riskType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postRiskType(data):
    row = riskType(title = data['title'],
                   desc = data['desc'],
                   tenant_uuid = session['tenant_uuid'],
                   uuid = UUID.uuid4(),
                   created=datetime.now(),
                   createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Risk Type added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Risk Type already exist'}
        else:
            return {'error': unicode(E)}

def putRiskType(data, uuid):
    row = getRiskType(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Risk Type updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Risk Type already exist'}
        else:
            return {'error': unicode(E)}

def deleteRiskType(uuid):
    entry = getRiskType(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Risk Type deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def riskTypeSelectData():
    data = getRiskTypes()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def riskTypeListData():
    entries = getRiskTypes()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
