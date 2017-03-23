## -*- coding: utf-8 -*-

from app import db
from flask import session
from app.treatment.models import treatment
import uuid as UUID
from datetime import datetime
from app.crud import treatmentTypeCrud, riskResponseCrud

def getTreatments():
    return treatment.query.filter_by(tenant_uuid=session['tenant_uuid']).all()

def getTreatment(uuid):
    return treatment.query.filter_by(uuid=uuid, tenant_uuid=session['tenant_uuid']).first()

def postTreatment(data):
    t = treatmentTypeCrud.getTreatmentType(data['treatmentType'])
    if t == None:
        treatmentType_uuid = None
    else:
        treatmentType_uuid = t.uuid

    r = riskResponseCrud.getRiskResponse(data['riskResponse'])
    if r == None:
        riskResponse_uuid = None
    else:
        riskResponse_uuid = r.uuid

    row = treatment(title = data['title'],
                        desc = data['desc'],
                        tenant_uuid = session['tenant_uuid'],
                        uuid = UUID.uuid4(),
                        treatmentType_uuid=treatmentType_uuid,
                        treatmentType=t,
                        riskResponse_uuid=riskResponse_uuid,
                        riskResponse=r,
                        created=datetime.now(),
                        createdBy=session['user_uuid'])

    try:
        db.session.add(row)
        db.session.commit()
        return {'success': 'Treatment added'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Treatment already exist'}
        else:
            return {'error': unicode(E)}

def putTreatment(data, uuid):
    t = treatmentTypeCrud.getTreatmentType(data['treatmentType'])
    if t == None:
        treatmentType_uuid = None
    else:
        treatmentType_uuid = t.uuid

    r = riskResponseCrud.getRiskResponse(data['riskResponse'])
    if r == None:
        riskResponse_uuid = None
    else:
        riskResponse_uuid = r.uuid

    row = getTreatment(uuid)

    row.title = data['title']
    row.desc = data['desc']
    row.modified = datetime.now()
    row.modifiedBy = session['user_uuid']
    row.treatmentType_uuid = treatmentType_uuid
    row.treatmentType = t
    row.riskResponse_uuid = riskResponse_uuid
    row.riskResponse = r

    try:
        db.session.commit()
        return {'success': 'Treatment updated'}
    except Exception as E:
        if 'unique constraint' in unicode(E):
            return {'error': 'Treatment already exist'}
        else:
            return {'error': unicode(E)}

def deleteTreatment(uuid):
    entry = getTreatment(uuid)
    try:
        db.session.delete(entry)
        db.session.commit()
        return {'success': 'Treatment deleted'}
    except Exception as E:
        return {'error': unicode(E)}

def treatmentSelectData():
    data = getTreatments()
    dataList = []
    for r in data:
        dataList.append((r.uuid, r.title))
    return dataList

def treatmentListData():
    entries = getTreatments()
    data = []
    for r in entries:
        temp = [r.uuid, r.title, r.desc, r.treatmentType.title, r.riskResponse.title]
        data.append(temp)
    return data
