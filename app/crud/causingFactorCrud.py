from app import db
from flask import session
from app.masterData.models import causingFactor
import uuid as UUID
from datetime import datetime

def getCausingFactors():
    return causingFactor.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getCausingFactor(uuid):
    return causingFactor.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postCausingFactor(data):
    row = causingFactor(title = data['title'],
                        desc = data['desc'],
                        tenant_uuid = session['tenant_uuid'],
                        uuid = UUID.uuid4(),
                        created=datetime.now(),
                        createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Causing Factor added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Causing Factor already exist'}
        else:
            return {'error': unicode(E)}

def putCausingFactor(data, uuid):
    row = getCausingFactor(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Causing Factor updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Causing Factor already exist'}
        else:
            return {'error': unicode(E)}

def deleteCausingFactor(uuid):
    entry = getCausingFactor(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Causing Factor deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def causingFactorSelectData():
    data = getCausingFactors()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def causingFactorListData():
    entries = getCausingFactors()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
