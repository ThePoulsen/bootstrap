from app import db
from flask import session
from app.masterData.models import causingFactorType
import uuid as UUID
from datetime import datetime

def getCausingFactorTypes():
    return causingFactorType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getCausingFactorType(uuid):
    return causingFactorType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postCausingFactorType(data):
    row = causingFactorType(title = data['title'],
                        desc = data['desc'],
                        tenant_uuid = session['tenant_uuid'],
                        uuid = UUID.uuid4(),
                        created=datetime.now(),
                        createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Causing Factor Type added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Causing Factor Type already exist'}
        else:
            return {'error': unicode(E)}

def putCausingFactorType(data, uuid):
    row = getCausingFactorType(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Causing Factor Type updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Causing Factor Type already exist'}
        else:
            return {'error': unicode(E)}

def deleteCausingFactorType(uuid):
    entry = getCausingFactorType(uuid)
    if entry.causingFactors:
        return {'error': 'Causing Factor Type cannot be deleted as long as there are Causing Factors assigned this Causing Factor Type'}
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Causing Factor Type deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def causingFactorTypeSelectData():
    data = getCausingFactorTypes()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def causingFactorTypeListData():
    entries = getCausingFactorTypes()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
