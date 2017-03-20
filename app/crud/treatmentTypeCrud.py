from app import db
from flask import session
from app.masterData.models import treatmentType
import uuid as UUID
from datetime import datetime

def getTreatmentTypes():
    return treatmentType.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getTreatmentType(uuid):
    return treatmentType.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postTreatmentType(data):
    row = treatmentType(title = data['title'],
                      desc = data['desc'],
                      tenant_uuid = session['tenant_uuid'],
                      uuid = UUID.uuid4(),
                      created=datetime.now(),
                      createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Treatment Type added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Treatment Type already exist'}
        else:
            return {'error': unicode(E)}

def putTreatmentType(data, uuid):
    row = getTreatmentType(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']

    try:
        db.session.commit()
        return {'success': 'Treatment Type updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Treatment Type already exist'}
        else:
            return {'error': unicode(E)}

def deleteTreatmentType(uuid):
    entry = getTreatmentType(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Treatment Type deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def treatmentTypeSelectData():
    data = getTreatmentTypes()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def treatmentTypeListData():
    entries = getTreatmentTypes()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc]
        data.append(temp)
    return data
